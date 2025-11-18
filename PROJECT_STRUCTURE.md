# Project Structure

```
bulksender/
├── bulkmailer/                    # Main package
│   ├── __init__.py
│   ├── cli.py                     # CLI entry point with Click
│   │
│   ├── auth/                      # Gmail OAuth authentication
│   │   ├── __init__.py
│   │   └── gmail_auth.py         # OAuth flow and token management
│   │
│   ├── file_loader/              # File loading (CSV/Excel)
│   │   ├── __init__.py
│   │   └── loader.py             # Pandas-based file reader
│   │
│   ├── template_engine/          # Template processing
│   │   ├── __init__.py
│   │   └── engine.py             # Placeholder replacement logic
│   │
│   ├── sender/                   # Email sending
│   │   ├── __init__.py
│   │   └── gmail_sender.py       # Gmail API sending with retries
│   │
│   ├── status_writer/            # Status tracking
│   │   ├── __init__.py
│   │   └── writer.py             # File saving with status column
│   │
│   └── logging_utils/            # Logging
│       ├── __init__.py
│       └── logger.py             # Console and file logging
│
├── tests/                         # Test directory (empty for now)
│
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup script
├── .gitignore                     # Git ignore rules
│
├── README.md                      # Full documentation
├── QUICKSTART.md                  # Quick start guide
├── PRD.md                         # Product requirements document
├── PROJECT_STRUCTURE.md           # This file
│
├── example_data.csv               # Sample CSV file
└── example_template.txt           # Sample email template

Files created at runtime:
├── credentials.json               # OAuth credentials (user provides)
└── token.pickle                   # Saved OAuth token (auto-generated)
```

## Module Responsibilities

### cli.py
- Parses command-line arguments with Click
- Coordinates the entire send workflow
- Manages exit codes
- Handles top-level error catching

### auth/gmail_auth.py
- Manages Google OAuth 2.0 flow
- Loads/saves token.pickle
- Refreshes expired tokens
- Returns authenticated Gmail service

### file_loader/loader.py
- Loads CSV and Excel files with pandas
- Validates required columns (name, email)
- Auto-detects or creates status column
- Returns FileData object

### template_engine/engine.py
- Extracts placeholders from templates
- Validates placeholders against available columns
- Renders templates with row data
- Handles missing placeholder values

### sender/gmail_sender.py
- Creates MIME email messages
- Sends via Gmail API
- Implements retry logic (3 attempts)
- Detects rate limits (429, 403 codes)
- Returns SendResult with status

### status_writer/writer.py
- Saves CSV files (overwrites original)
- Saves Excel files (creates _updated or overwrites)
- Handles file locking gracefully

### logging_utils/logger.py
- Prints to console
- Optionally logs to file with timestamps
- Provides structured log methods
- Tracks success/failure/skip counts

## Data Flow

1. **CLI** receives arguments
2. **File Loader** loads and validates data
3. **Auth** authenticates with Gmail
4. For each row:
   - **Template Engine** renders subject and body
   - **Sender** attempts to send email
   - **Logger** records result
   - Status updated in dataframe
5. **Status Writer** saves updated file
6. **Logger** prints summary
7. **CLI** exits with appropriate code

## Exit Codes

- `0` - Success
- `1` - Missing required flags
- `2` - Gmail rate limit
- `3` - File error
- `4` - Unexpected error
