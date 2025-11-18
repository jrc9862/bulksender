"""Logger for tracking email sending progress"""
import sys
from datetime import datetime
from typing import Optional


class Logger:
    """Logger that prints to console and optionally to a file"""

    def __init__(self, log_file: Optional[str] = None):
        """
        Initialize logger.

        Args:
            log_file: Optional path to log file
        """
        self.log_file = log_file
        self.log_handle = None

        if self.log_file:
            try:
                self.log_handle = open(self.log_file, 'a', encoding='utf-8')
            except Exception as e:
                print(f"Warning: Could not open log file: {e}", file=sys.stderr)
                self.log_handle = None

    def log(self, message: str, to_file_only: bool = False):
        """
        Log a message to console and/or file.

        Args:
            message: Message to log
            to_file_only: If True, only write to file, not console
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        formatted = f"[{timestamp}] {message}"

        if not to_file_only:
            print(message)

        if self.log_handle:
            try:
                self.log_handle.write(formatted + '\n')
                self.log_handle.flush()
            except Exception as e:
                print(f"Warning: Could not write to log file: {e}", file=sys.stderr)

    def log_success(self, row_idx: int, email: str):
        """Log successful email send"""
        self.log(f"Row {row_idx}: Sent to {email}")

    def log_failure(self, row_idx: int, email: str, reason: str):
        """Log failed email send"""
        self.log(f"Row {row_idx}: Failed to send to {email} - {reason}")

    def log_skip(self, row_idx: int, reason: str):
        """Log skipped row"""
        self.log(f"Row {row_idx}: Skipped - {reason}")

    def log_summary(self, total: int, sent: int, failed: int, skipped: int):
        """Log final summary"""
        self.log("\n" + "="*50)
        self.log("SUMMARY")
        self.log("="*50)
        self.log(f"Total rows processed: {total}")
        self.log(f"Successfully sent: {sent}")
        self.log(f"Failed: {failed}")
        self.log(f"Skipped: {skipped}")
        self.log("="*50)

    def log_rate_limit(self, last_successful_row: int):
        """Log rate limit interruption"""
        self.log("\n" + "!"*50)
        self.log("RATE LIMIT REACHED")
        self.log("!"*50)
        self.log(f"Last successfully processed row: {last_successful_row}")
        self.log("File has been saved with current progress.")
        self.log("Please wait before resuming the operation.")
        self.log("!"*50)

    def close(self):
        """Close the log file handle"""
        if self.log_handle:
            try:
                self.log_handle.close()
            except Exception:
                pass
