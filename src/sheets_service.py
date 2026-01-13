import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import CREDENTIALS_PATH, TOKEN_PATH, SCOPES

def get_sheets_service():
    """Shows basic usage of the Sheets API.
    Returns an authenticated Sheets service object.
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

    service = build('sheets', 'v4', credentials=creds)
    return service

def append_to_sheet(service, spreadsheet_id, values):
    """
    Appends a row of values to the spreadsheet.
    values: list of strings [From, Subject, Date, Content]
    """
    try:
        body = {
            'values': [values]
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A:D',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"{result.get('updates').get('updatedCells')} cells appended.")
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
