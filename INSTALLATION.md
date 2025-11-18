# Installation Guide

## Prerequisites

- Python 3.13 or higher
- Gmail account
- Google Cloud Project with Gmail API enabled

## Step 1: Clone/Download the Project

If you haven't already, navigate to the project directory:

```bash
cd /home/james/Coding\ Projects/bulksender
```

## Step 2: Create Virtual Environment

Using standard Python venv:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Or using uv (faster):

```bash
uv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or with uv:

```bash
uv pip install -r requirements.txt
```

## Step 4: Set Up Gmail API

### 4.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name (e.g., "Bulk Mailer")
4. Click "Create"

### 4.2 Enable Gmail API

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on it and press "Enable"

### 4.3 Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: Your app name
   - User support email: Your email
   - Developer contact: Your email
   - Click "Save and Continue"
   - Scopes: Skip (click "Save and Continue")
   - Test users: Add your Gmail address
   - Click "Save and Continue"
4. Back in "Create OAuth client ID":
   - Application type: "Desktop app"
   - Name: "Bulk Mailer Desktop"
   - Click "Create"
5. Click "Download JSON"
6. Save the downloaded file as `credentials.json` in the project root directory

### 4.4 Directory Structure After Setup

```
bulksender/
├── credentials.json  ← Your OAuth credentials (keep private!)
├── bulkmailer/
├── requirements.txt
└── ...
```

## Step 5: Test Installation

Test that everything is installed correctly:

```bash
python3 -m bulkmailer.cli --help
```

You should see the help message with available commands.

## Step 6: First Run (Dry Run)

Test with the example files:

```bash
python3 -m bulkmailer.cli send \
  --file example_data.csv \
  --subject "Hello {name}" \
  --body example_template.txt \
  --dry-run
```

This will show how emails will look without sending anything.

## Step 7: Authenticate

Run your first real send (with limit):

```bash
python3 -m bulkmailer.cli send \
  --file example_data.csv \
  --subject "Test email for {name}" \
  --body example_template.txt \
  --limit 1
```

This will:
1. Open your browser
2. Ask you to sign in to Gmail
3. Ask you to authorize the app
4. Save the token locally as `token.pickle`
5. Send 1 test email

## Optional: Install as System Command

To use `bulkmailer` command directly (instead of `python3 -m bulkmailer.cli`):

```bash
pip install -e .
```

Now you can use:

```bash
bulkmailer send --file data.csv --subject "Hi {name}" --body template.txt
```

## Troubleshooting

### "Module not found" errors

Make sure your virtual environment is activated:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### "credentials.json not found"

Make sure the file is in the project root directory (same level as requirements.txt).

### OAuth consent screen warnings

If you see warnings about unverified app:
1. Click "Advanced"
2. Click "Go to [Your App Name] (unsafe)"
3. This is normal for personal projects

### Permission denied errors

Make sure you have write permissions in the directory.

## Security Notes

**Never commit these files:**
- `credentials.json` - Your OAuth client credentials
- `token.pickle` - Your access token

These are already listed in `.gitignore`.

**Keep them secure:**
- Don't share them
- Don't upload to public repositories
- Store in secure location

## Next Steps

- Read [QUICKSTART.md](QUICKSTART.md) for usage examples
- Read [README.md](README.md) for full documentation
- Prepare your CSV/Excel file with recipient data
- Write your email template
- Start sending!
