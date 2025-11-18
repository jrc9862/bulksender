"""CLI interface for bulkmailer"""
import sys
import os
import re
import click
import pandas as pd
from .auth import authenticate_gmail
from .file_loader import load_file
from .template_engine import render_template
from .sender import send_email
from .status_writer import save_file_with_status
from .logging_utils import Logger

# Exit codes
EXIT_SUCCESS = 0
EXIT_MISSING_FLAGS = 1
EXIT_RATE_LIMIT = 2
EXIT_FILE_ERROR = 3
EXIT_UNEXPECTED = 4


def validate_email(email: str) -> bool:
    """Validate email format using simple regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, str(email)) is not None


@click.group()
def cli():
    """Local Gmail Bulk Mailer CLI"""
    pass


@cli.command()
@click.option('--file', required=True, type=click.Path(exists=True), help='Path to CSV or Excel file')
@click.option('--subject', required=True, help='Email subject with {placeholders}')
@click.option('--body', required=True, type=click.Path(exists=True), help='Path to email body template file')
@click.option('--log', type=click.Path(), help='Optional log file path')
@click.option('--inplace', is_flag=True, help='For Excel files, overwrite original instead of creating new file')
@click.option('--limit', type=int, help='Limit number of emails to send (for testing)')
@click.option('--dry-run', is_flag=True, help='Preview rendered emails without sending')
def send(file, subject, body, log, inplace, limit, dry_run):
    """Send personalized bulk emails via Gmail"""
    logger = Logger(log)

    try:
        # Load body template
        logger.log(f"Loading body template from {body}...")
        try:
            with open(body, 'r', encoding='utf-8') as f:
                body_template = f.read()
        except Exception as e:
            logger.log(f"Error: Could not read body template: {e}")
            sys.exit(EXIT_FILE_ERROR)

        # Load data file
        logger.log(f"Loading data file from {file}...")
        try:
            file_data = load_file(file)
        except FileNotFoundError as e:
            logger.log(f"Error: {e}")
            sys.exit(EXIT_FILE_ERROR)
        except ValueError as e:
            logger.log(f"Error: {e}")
            sys.exit(EXIT_FILE_ERROR)
        except Exception as e:
            logger.log(f"Error loading file: {e}")
            sys.exit(EXIT_FILE_ERROR)

        df = file_data.df
        status_column = file_data.status_column
        logger.log(f"Loaded {len(df)} rows from file")
        logger.log(f"Status column: {status_column}")

        # Authenticate with Gmail (skip in dry-run)
        service = None
        if not dry_run:
            logger.log("Authenticating with Gmail...")
            try:
                service = authenticate_gmail()
                logger.log("Authentication successful")
            except FileNotFoundError as e:
                logger.log(f"Error: {e}")
                sys.exit(EXIT_MISSING_FLAGS)
            except Exception as e:
                logger.log(f"Error authenticating: {e}")
                sys.exit(EXIT_UNEXPECTED)

        # Process rows
        logger.log("\nStarting processing...")
        logger.log("-" * 50)

        sent_count = 0
        failed_count = 0
        skipped_count = 0
        last_successful_row = -1
        rate_limited = False

        for idx, row in df.iterrows():
            # Check limit
            if limit and (sent_count + failed_count) >= limit:
                logger.log(f"\nReached limit of {limit} emails")
                break

            # Check if already processed
            current_status = row.get(status_column, '')
            if current_status == 'sent':
                logger.log_skip(idx, "Already sent")
                skipped_count += 1
                continue

            # Validate email
            email = row.get('email')
            if pd.isna(email) or not email:
                logger.log_failure(idx, 'N/A', "Missing email address")
                df.at[idx, status_column] = 'failed'
                failed_count += 1
                continue

            if not validate_email(email):
                logger.log_failure(idx, email, "Invalid email format")
                df.at[idx, status_column] = 'failed'
                failed_count += 1
                continue

            # Get name
            name = row.get('name')
            if pd.isna(name) or not name:
                logger.log_failure(idx, email, "Missing name")
                df.at[idx, status_column] = 'failed'
                failed_count += 1
                continue

            # Prepare row data for template rendering
            row_data = row.to_dict()

            # Render subject
            rendered_subject, subject_success, subject_missing = render_template(subject, row_data)
            if not subject_success:
                logger.log_failure(idx, email, f"Missing subject placeholders: {', '.join(subject_missing)}")
                df.at[idx, status_column] = 'failed'
                failed_count += 1
                continue

            # Render body
            rendered_body, body_success, body_missing = render_template(body_template, row_data)
            if not body_success:
                logger.log_failure(idx, email, f"Missing body placeholders: {', '.join(body_missing)}")
                df.at[idx, status_column] = 'failed'
                failed_count += 1
                continue

            # Dry run mode - just print
            if dry_run:
                logger.log(f"\n--- Row {idx} ---")
                logger.log(f"To: {email}")
                logger.log(f"Subject: {rendered_subject}")
                logger.log(f"Body:\n{rendered_body}")
                logger.log("-" * 50)
                sent_count += 1
                continue

            # Send email
            result = send_email(service, email, rendered_subject, rendered_body)

            if result.success:
                logger.log_success(idx, email)
                df.at[idx, status_column] = 'sent'
                sent_count += 1
                last_successful_row = idx
            elif result.rate_limited:
                # Rate limit hit - stop immediately
                logger.log_failure(idx, email, result.error_message)
                rate_limited = True
                break
            else:
                logger.log_failure(idx, email, result.error_message)
                df.at[idx, status_column] = 'failed'
                failed_count += 1

        # Save file with status updates
        if not dry_run:
            logger.log("\nSaving file with status updates...")
            try:
                saved_path = save_file_with_status(file_data, inplace)
                logger.log(f"File saved: {saved_path}")
            except Exception as e:
                logger.log(f"Error saving file: {e}")
                sys.exit(EXIT_FILE_ERROR)

        # Print summary
        total_processed = sent_count + failed_count + skipped_count
        logger.log_summary(total_processed, sent_count, failed_count, skipped_count)

        # Handle rate limit exit
        if rate_limited:
            logger.log_rate_limit(last_successful_row)
            logger.close()
            sys.exit(EXIT_RATE_LIMIT)

        logger.close()
        sys.exit(EXIT_SUCCESS)

    except Exception as e:
        logger.log(f"Unexpected error: {e}")
        import traceback
        logger.log(traceback.format_exc())
        logger.close()
        sys.exit(EXIT_UNEXPECTED)


if __name__ == '__main__':
    cli()
