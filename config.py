import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Credentials
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials', 'credentials.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'credentials', 'token.json')

# API Scopes
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets'
]

# Spreadsheet ID (will be needed later, placeholder for now)
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE'
