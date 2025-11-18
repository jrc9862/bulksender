# Quick Start Guide

## 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Set Up Gmail API

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as `credentials.json` and place in project root

## 3. Test with Dry Run

Use the included example files:

```bash
python -m bulkmailer.cli send \
  --file example_data.csv \
  --subject "Hello {name} from {company}" \
  --body example_template.txt \
  --dry-run
```

This will show you how emails will look without actually sending them.

## 4. Send Real Emails (with limit)

First, test with just 1 email:

```bash
python -m bulkmailer.cli send \
  --file example_data.csv \
  --subject "Hello {name}" \
  --body example_template.txt \
  --limit 1
```

The first time you run this:
- A browser window will open
- Sign in to your Gmail account
- Authorize the application
- The token will be saved locally

## 5. Send All Emails

Once tested, send to all recipients:

```bash
python -m bulkmailer.cli send \
  --file your_data.csv \
  --subject "Your subject with {placeholders}" \
  --body your_template.txt \
  --log output.log
```

## 6. Check Results

- CSV files are updated with status column automatically
- Excel files create a new `*_updated.xlsx` file (unless you use `--inplace`)
- Check the log file for detailed information

## Tips

- Always test with `--dry-run` first
- Use `--limit 5` to test with a small batch
- The tool automatically skips rows already marked as "sent"
- If rate limited, just wait and re-run the same command

## Common Issues

**"credentials.json not found"**
- Make sure you downloaded OAuth credentials from Google Cloud Console

**"Module not found"**
- Activate your virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

**Email not found in sent folder**
- Check Gmail's "Sent" folder
- May take a few minutes to appear
- Check spam/promotions tab for recipient

## Security Note

Never commit these files to version control:
- `credentials.json` (your OAuth client credentials)
- `token.pickle` (your access token)

These are already in `.gitignore`.
