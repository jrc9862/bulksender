# Pre-Launch Checklist

Use this checklist before sending your first batch of emails.

## Setup (One-Time)

- [ ] Python 3.13+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Google Cloud Project created
- [ ] Gmail API enabled in Google Cloud Console
- [ ] OAuth credentials downloaded as `credentials.json`
- [ ] `credentials.json` placed in project root directory

## Data Preparation

- [ ] CSV or Excel file prepared with data
- [ ] File has `name` column
- [ ] File has `email` column
- [ ] Email addresses are valid
- [ ] Additional columns added for personalization (optional)
- [ ] No sensitive data that shouldn't be sent

## Email Template

- [ ] Subject line written with placeholders (e.g., "Hello {name}")
- [ ] Body template saved as .txt file
- [ ] Body template uses correct placeholder format `{column_name}`
- [ ] All placeholders match column names in your data file
- [ ] Template is professional and error-free
- [ ] No typos or grammar mistakes

## Testing

- [ ] Ran with `--dry-run` to preview emails
- [ ] Checked that placeholders are replaced correctly
- [ ] Verified email content looks good
- [ ] Tested with `--limit 1` to send one test email
- [ ] Received test email successfully
- [ ] Test email looks correct in inbox
- [ ] Test email not in spam folder

## Gmail Setup

- [ ] Authenticated (browser OAuth flow completed)
- [ ] `token.pickle` file created successfully
- [ ] Test email sent successfully
- [ ] Sender address is correct (your Gmail)

## Production Readiness

- [ ] Data file is final version
- [ ] All recipient emails are correct
- [ ] Template is final version
- [ ] Decided on logging (`--log` flag)
- [ ] Decided on file handling (`--inplace` for Excel)
- [ ] Ready to send all emails

## Launch Command Ready

Your command should look like:

```bash
python3 -m bulkmailer.cli send \
  --file YOUR_DATA_FILE.csv \
  --subject "YOUR SUBJECT WITH {placeholders}" \
  --body YOUR_TEMPLATE.txt \
  --log output.log
```

## Post-Send

- [ ] Check console output for errors
- [ ] Review log file if enabled
- [ ] Check status column in data file
- [ ] Verify sent count matches expectations
- [ ] Spot-check a few emails were delivered

## If Rate Limited

- [ ] Note the last successful row number
- [ ] Wait 15-30 minutes (or per Gmail guidelines)
- [ ] Re-run the same command (will skip already-sent)
- [ ] Monitor for successful resume

## Common Mistakes to Avoid

- ❌ Not testing with `--dry-run` first
- ❌ Forgetting to check for typos in template
- ❌ Using wrong column names in placeholders
- ❌ Not having `credentials.json` in correct location
- ❌ Sending to wrong email list
- ❌ Not backing up original data file
- ❌ Exceeding Gmail sending limits (typically 500/day for free accounts)

## Gmail Sending Limits

**Be aware of Gmail's limits:**
- Free accounts: ~500 emails per day
- Google Workspace: ~2,000 emails per day
- Limits are per 24-hour rolling period

**Tips:**
- Use `--limit` to stay under daily quota
- Spread large campaigns over multiple days
- Monitor for rate limit warnings

## Emergency Stop

If you need to stop while sending:
- Press `Ctrl+C` in terminal
- The current row may still send
- File will be saved with progress so far
- You can resume by running the same command

## Support

If you encounter issues:
1. Check the error message carefully
2. Review INSTALLATION.md for setup issues
3. Review README.md for usage issues
4. Check that all placeholders are spelled correctly
5. Verify your data file has required columns

## Ready to Go?

If all boxes are checked, you're ready to send!

```bash
# Activate virtual environment
source venv/bin/activate

# Run your send command
python3 -m bulkmailer.cli send --file YOUR_FILE.csv --subject "..." --body template.txt --log output.log
```

Good luck!
