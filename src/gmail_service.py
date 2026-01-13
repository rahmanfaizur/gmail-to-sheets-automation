import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import CREDENTIALS_PATH, TOKEN_PATH, SCOPES

def get_gmail_service():
    """Shows basic usage of the Gmail API.
    Returns an authenticated Gmail service object.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

def fetch_unread_emails(service):
    """
    Fetches unread emails from the inbox.
    Returns a list of message objects (containing IDs).
    """
    try:
        results = service.users().messages().list(
            userId='me',
            q='is:unread in:inbox'
        ).execute()
        
        messages = results.get('messages', [])
        return messages
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def mark_as_read(service, message_ids):
    """Marks a list of emails as read."""
    if not message_ids:
        return
    
    try:
        service.users().messages().batchModify(
            userId='me',
            body={
                'ids': message_ids,
                'removeLabelIds': ['UNREAD']
            }
        ).execute()
        print(f"Marked {len(message_ids)} emails as read.")
    except Exception as e:
        print(f"Error marking emails as read: {e}")
