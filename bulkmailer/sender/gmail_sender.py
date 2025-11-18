"""Gmail sender with retry logic and rate limit detection"""
import base64
import time
from email.mime.text import MIMEText
from dataclasses import dataclass
from typing import Optional
from googleapiclient.errors import HttpError


@dataclass
class SendResult:
    """Result of sending an email"""
    success: bool
    error_message: Optional[str] = None
    rate_limited: bool = False


def create_message(to: str, subject: str, body: str) -> dict:
    """
    Create a message for an email.

    Args:
        to: Email address of the receiver
        subject: The subject of the email
        body: The body text of the email

    Returns:
        An object containing a base64url encoded email
    """
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}


def send_email(service, to: str, subject: str, body: str, max_retries: int = 3) -> SendResult:
    """
    Send an email via Gmail API with retry logic.

    Args:
        service: Authenticated Gmail API service object
        to: Recipient email address
        subject: Email subject
        body: Email body
        max_retries: Maximum number of retry attempts for transient errors

    Returns:
        SendResult indicating success/failure and any error details
    """
    message = create_message(to, subject, body)

    for attempt in range(max_retries):
        try:
            service.users().messages().send(userId='me', body=message).execute()
            return SendResult(success=True)

        except HttpError as e:
            error_details = e.error_details if hasattr(e, 'error_details') else []
            status_code = e.resp.status

            # Check for rate limiting (429 or 403 with specific reason)
            if status_code == 429:
                return SendResult(
                    success=False,
                    error_message=f"Rate limit exceeded: {str(e)}",
                    rate_limited=True
                )

            # Check for quota exceeded (403 with userRateLimitExceeded)
            if status_code == 403:
                for detail in error_details:
                    if detail.get('reason') in ['userRateLimitExceeded', 'rateLimitExceeded', 'quotaExceeded']:
                        return SendResult(
                            success=False,
                            error_message=f"Gmail rate limit: {str(e)}",
                            rate_limited=True
                        )

            # Check for transient errors (500, 503)
            if status_code in [500, 503] and attempt < max_retries - 1:
                # Wait before retrying (exponential backoff)
                wait_time = 2 ** attempt
                time.sleep(wait_time)
                continue

            # Other errors - don't retry
            return SendResult(
                success=False,
                error_message=f"HTTP Error {status_code}: {str(e)}",
                rate_limited=False
            )

        except Exception as e:
            # Unexpected error
            return SendResult(
                success=False,
                error_message=f"Unexpected error: {str(e)}",
                rate_limited=False
            )

    # If we exhausted all retries
    return SendResult(
        success=False,
        error_message=f"Failed after {max_retries} attempts",
        rate_limited=False
    )
