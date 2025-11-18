# Local Gmail Bulk Mailer CLI

A privacy-preserving command-line tool for sending personalized bulk emails via Gmail API. All processing happens locally on your machine.

## Features

- Import CSV or Excel (.xlsx) files with recipient data
- Personalize emails using template placeholders like `{name}`, `{company}`, etc.
- Gmail OAuth authentication (no password storage)
- Track send status for each row (sent/failed)
- Automatic rate limit detection with graceful shutdown
- Dry-run mode to preview emails before sending
- Optional logging to file
- Retry logic for transient network errors

## Installation

1. Clone or download this repository
2. Create a virtual environment and install dependencies:

```bash
# Using uv (recommended)
uv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
uv pip install -r requirements.txt

# Or using standard pip
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Gmail API Setup

Before using this tool, you need to set up Gmail API credentials:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Gmail API for your project
4. Go to "Credentials" and create OAuth 2.0 Client ID credentials
5. Download the credentials and save as `credentials.json` in the project root directory

On first run, the tool will open a browser window for you to authorize access. The token will be saved locally as `token.pickle`.

## Usage

### Basic Command

```bash
python -m bulkmailer.cli send --file data.csv --subject "Hello {name}" --body template.txt
```

### Command Options

```
Required:
  --file PATH        Path to CSV or Excel file with recipient data
  --subject TEXT     Email subject with {placeholder} format
  --body PATH        Path to text file containing email body template

Optional:
  --log PATH         Path to log file for detailed logging
  --inplace          Overwrite original Excel file (default: create new file)
  --limit N          Limit number of emails to send (useful for testing)
  --dry-run          Preview rendered emails without sending
```

### File Format

Your CSV or Excel file must have these required columns:
- `name`: Recipient name
- `email`: Recipient email address

You can include additional columns for personalization.

**Example CSV:**

```csv
name,email,company,position
John Doe,john@example.com,Acme Corp,Manager
Jane Smith,jane@example.com,Tech Inc,Developer
```

### Template Format

Use `{column_name}` syntax for placeholders.

**Example subject:**
```
Hello {name}, opportunities at {company}
```

**Example body template (template.txt):**
```
Hi {name},

I hope this email finds you well. I noticed you work as a {position} at {company}.

I wanted to reach out regarding...

Best regards
```

### Examples

**Preview emails without sending:**
```bash
python -m bulkmailer.cli send --file contacts.csv --subject "Hi {name}" --body message.txt --dry-run
```

**Send emails with logging:**
```bash
python -m bulkmailer.cli send --file contacts.csv --subject "Hi {name}" --body message.txt --log output.log
```

**Test with first 5 recipients:**
```bash
python -m bulkmailer.cli send --file contacts.csv --subject "Hi {name}" --body message.txt --limit 5
```

**Overwrite Excel file in place:**
```bash
python -m bulkmailer.cli send --file data.xlsx --subject "Hi {name}" --body message.txt --inplace
```

## Status Tracking

The tool automatically adds a status column to track sending progress:
- Blank: Not yet processed
- `sent`: Email sent successfully
- `failed`: Email failed to send (with reason logged)

For CSV files, the original file is updated. For Excel files, a new file with `_updated` suffix is created (unless `--inplace` is used).

If you re-run the tool, rows marked as `sent` will be skipped automatically.

## Rate Limiting

When Gmail rate limits are detected, the tool will:
1. Immediately stop processing
2. Save the file with current status updates
3. Report the last successfully processed row
4. Exit with code 2

You can resume by running the same command again after waiting. Already-sent emails will be skipped.

## Exit Codes

- `0`: Success
- `1`: Missing required flags
- `2`: Gmail rate limit reached
- `3`: File error
- `4`: Unexpected error

## Security & Privacy

- All data processing happens locally
- OAuth tokens stored locally in `token.pickle`
- No passwords are stored or transmitted
- Contact data never leaves your machine except for Gmail API calls
- Add `token.pickle` and `credentials.json` to `.gitignore` (already configured)

## Limitations

- Attachments are not supported
- Maximum file size depends on available memory (designed for up to 50,000 rows)
- Subject to Gmail sending limits (typically 500 emails per day for free accounts)

## Troubleshooting

**"credentials.json not found"**
- Download OAuth credentials from Google Cloud Console and place in project root

**"Rate limit exceeded"**
- Wait a few minutes/hours and re-run the command
- Gmail has daily sending limits

**"Invalid email format"**
- Check that email addresses in your file are valid

**Import errors**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`

## Project Structure

```
bulksender/
├── bulkmailer/
│   ├── __init__.py
│   ├── cli.py                 # Main CLI interface
│   ├── auth/                  # Gmail OAuth authentication
│   ├── file_loader/           # CSV/Excel file loading
│   ├── template_engine/       # Placeholder replacement
│   ├── sender/                # Gmail API sending logic
│   ├── status_writer/         # Status tracking and file saving
│   └── logging_utils/         # Logging functionality
├── requirements.txt
├── .gitignore
└── README.md
```

## License

This project is provided as-is for personal and educational use.
