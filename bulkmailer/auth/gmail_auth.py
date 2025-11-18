"""Gmail OAuth authentication handler"""
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = 'token.pickle'
CREDENTIALS_FILE = 'credentials.json'


def authenticate_gmail():
    """
    Authenticate with Gmail using OAuth2.

    Returns:
        gmail service object

    Raises:
        FileNotFoundError: If credentials.json is not found
        Exception: If authentication fails
    """
    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # If credentials are invalid or don't exist, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh the token
            creds.refresh(Request())
        else:
            # Check if credentials.json exists
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"{CREDENTIALS_FILE} not found. Please download it from Google Cloud Console.\n"
                    "Visit: https://console.cloud.google.com/apis/credentials"
                )

            # Perform OAuth flow
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for future use
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    # Build and return the Gmail service
    service = build('gmail', 'v1', credentials=creds)
    return service
