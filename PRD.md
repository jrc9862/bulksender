# Local Gmail Bulk Mailer CLI PRD

## 1. Product Overview

A local command line tool that reads a CSV or Excel file containing recipients, personalizes email subject and body using row level data, authenticates with Gmail through OAuth, sends emails sequentially, marks each row as sent or failed, and halts immediately when Gmail rate limits occur while reporting the last successful row.

## 2. Problem Definition

Users need a privacy preserving way to send personalized emails at scale without cloud services or commercial bulk email platforms. Most available tools are either server based or lack template level personalization. This CLI preserves privacy because all logic runs locally and only Gmail API calls leave the device.

## 3. Goals

* Import CSV or Excel files.
* Personalize outgoing messages using placeholders.
* Authenticate and send through Gmail API.
* Track status per row within the file.
* Halt cleanly on Gmail rate limits.
* Keep everything local.

## 4. Scope

### Included

* CSV and Excel input.
* Gmail OAuth.
* Template processing.
* Per row status marking.
* Logging and CLI usage instructions.

### Excluded

* Attachments.
* GUI.
* SMTP password flows.

## 5. Core User Flow

1. User runs CLI with file path plus subject and body flags.
2. Tool loads the file and chooses or creates a status column.
3. Tool checks or initializes OAuth tokens.
4. Tool iterates rows in order.
5. Each row is validated, rendered, sent, and marked as sent or failed.
6. If Gmail rate limits occur, the tool stops, reports last successful row, saves updated file, and exits.
7. If the run completes, the tool reports totals and writes updated file.

## 6. Functional Requirements

### 6.1 File Input

* Accept CSV and Excel (.xlsx).
* Required columns: name and email.
* Support extra columns for placeholder expansion.
* If required data is missing for a row the row is processed and marked failed.
* Handle empty rows and malformed rows gracefully.

### 6.2 Template Handling

* Subject provided through the subject flag.
* Body loaded from a text file provided through the body flag.
* Placeholders use the format {column_name}.
* Missing placeholder values for a row mark that row failed.
* A dry run mode prints rendered messages without sending.

### 6.3 Gmail Authentication

* Use Google OAuth installed app flow.
* Store token locally in a token.json style file.
* Refresh tokens automatically.
* Never request or store passwords.

### 6.4 Sending Logic

* Process rows in order.
* Validate email formats.
* Validate placeholder availability.
* On per row failure mark failed and continue.
* On Gmail rate limit halt immediately, save file, return rate limit exit code.
* Retry transient network errors up to three times.

### 6.5 Status Tracking

* Auto detect first unused column header for status.
* Default name: status. If taken use status_1 then status_2 and so on.
* Row values: sent, failed, or blank.
* CSV is rewritten. Excel is saved as a new updated file unless the inplace flag is passed.

### 6.6 CLI Interface

Command:
bulkmailer send --file PATH --subject "Subject {name}" --body body.txt [options]

Required flags:

* file
* subject
* body

If a required flag is missing the tool exits immediately with usage instructions.

Optional flags:

* log
* inplace
* limit
* dry run

### 6.7 Logging

* Print per row status.
* Optional log file with timestamps.
* Summary printed on completion.
* On rate limit print the last successful row index.

### 6.8 Error Handling

* Missing subject or body causes immediate exit code 1.
* File access failures produce exit code 3.
* Gmail rate limit produces exit code 2.
* Unexpected errors produce exit code 4 while preserving file updates written so far.

## 7. Non Functional Requirements

### 7.1 Performance

* Support up to at least 50000 rows.
* Use streaming or chunk based reading and writing when possible.

### 7.2 Reliability

* Deterministic row order.
* No double sending unless user manually reruns.

### 7.3 Security

* No password storage.
* Only OAuth tokens stored locally.
* Template and contact data never leave the local environment except for Gmail API operations.

### 7.4 Portability

* Runs on Windows.
* Runs in WSL.

### 7.5 Maintainability

* Modular code structure for auth, file loading, templating, sending, status writing, logging, and CLI.
* Unit tests on critical modules.

### 7.6 Usability

* CLI help includes full example usage.
* Clear errors with hints to fix input issues.

## 8. System Architecture

### 8.1 Components

* CLI: parses arguments, coordinates run, manages exit codes.
* File Loader: detects file type, streams rows, loads headers.
* Template Engine: resolves placeholders per row.
* Gmail Sender: manages OAuth, handles send operations, interprets Gmail errors.
* Status Writer: updates status column in memory and writes final output file.
* Logger: prints and logs progress.

### 8.2 Data Flow

1. CLI reads arguments.
2. File Loader returns row iterator and metadata.
3. Auth ensures valid OAuth token.
4. Template Engine generates personalized subject and body.
5. Gmail Sender attempts transmission.
6. Status Writer applies row result.
7. Logger reports each step.
8. File is saved on completion or interruption.

## 9. Data Model

### 9.1 Row Data

* name: string
* email: string
* optional columns: arbitrary string values
* status: sent or failed or blank

### 9.2 OAuth Token

* access_token
* refresh_token
* expiry
* client_id
* client_secret

## 10. Command

bulkmailer send
Required flags: file, subject, body
Optional flags: log, inplace, limit, dry run

## 11. Validation

* Required flags must be present.
* File must exist.
* Template file must exist.

## 12. Edge Cases

* Empty file.
* Missing name or email.
* Duplicate email values.
* Missing placeholder values.
* Excel sheet locked during save.
* CSV with variable column counts.
* Gmail transient network failures.

## 13. Success Criteria

* All rows processed or halted on rate limit.
* All statuses written reliably.
* Clear progress and summary output.
* Predictable exit codes.
* No unintended email sends.

## 14. Development Plan

### 14.1 Environment

* Python 3.13 or higher.
* Virtual environment created with uv.
* All dependencies installed in venv.

### 14.2 Dependencies

* Google API Python client.
* Google OAuth client.
* pandas.
* openpyxl.
* click or argparse.
* Standard library for email formatting.

### 14.3 Repository Structure

project_root

* cli
* auth
* file_loader
* template_engine
* sender
* status_writer
* logging_utils
* tests
* requirements.txt
* .gitignore

### 14.4 Exit Codes

* 0 success.
* 1 missing required flags.
* 2 Gmail rate limit.
* 3 file error.
* 4 unexpected error.

