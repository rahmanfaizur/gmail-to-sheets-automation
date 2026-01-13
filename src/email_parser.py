import base64
import re
from datetime import datetime

def clean_text(text):
    """Removes extra whitespace and newlines."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def get_header_value(headers, name):
    """Extracts a specific header value."""
    for header in headers:
        if header['name'].lower() == name.lower():
            return header['value']
    return ""

def parse_email(message):
    """
    Parses a Gmail message object.
    Returns a dictionary with sender, subject, date, and body.
    """
    payload = message.get('payload', {})
    headers = payload.get('headers', [])
    
    sender = get_header_value(headers, 'From')
    subject = get_header_value(headers, 'Subject')
    date_str = get_header_value(headers, 'Date')
    
    # Simple date cleanup (optional, can be improved)
    # date_str often looks like "Tue, 13 Jan 2026 16:41:46 +0530"
    
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
                    break
    else:
        # Fallback for non-multipart emails
        data = payload.get('body', {}).get('data')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8')

    return {
        'sender': clean_text(sender),
        'subject': clean_text(subject),
        'date': clean_text(date_str),
        'body': clean_text(body)
    }
