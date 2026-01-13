import json
import os
from config import BASE_DIR

STATE_FILE = os.path.join(BASE_DIR, 'state.json')

def load_state():
    """
    Loads the last processed historyId from state.json.
    We use historyId to efficiently track changes in the mailbox
    and avoid processing the same email twice.
    """
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_state(history_id):
    """
    Saves the current historyId to state.json.
    This should be called only after successful processing.
    """
    with open(STATE_FILE, 'w') as f:
        json.dump({'historyId': history_id}, f)

from gmail_service import get_gmail_service, fetch_unread_emails, mark_as_read
from sheets_service import get_sheets_service, append_to_sheet
from email_parser import parse_email
from config import SPREADSHEET_ID

def main():
    print("🚀 Starting Gmail to Sheets automation...")

    # 1. Authenticate
    print("🔑 Authenticating services...")
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service()

    # 2. Load State
    state = load_state()
    last_history_id = state.get('historyId')
    print(f"📜 Loaded state: Last historyId = {last_history_id}")

    # 3. Fetch Emails
    print("📨 Fetching unread emails...")
    messages = fetch_unread_emails(gmail_service)
    
    if not messages:
        print("📭 No new unread emails found.")
        return

    print(f"📬 Found {len(messages)} unread emails.")

    if not SPREADSHEET_ID or SPREADSHEET_ID == 'YOUR_SPREADSHEET_ID_HERE':
        print("⚠️  WARNING: SPREADSHEET_ID is not set in config.py.")
        print("Please create a sheet and add its ID to config.py.")
        return

    processed_count = 0
    message_ids_to_mark = []

    for msg in messages:
        # 4. Parse Email
        # We need to fetch the full details first
        full_msg = gmail_service.users().messages().get(userId='me', id=msg['id']).execute()
        
        email_data = parse_email(full_msg)
        print(f"   Processing: {email_data['subject'][:30]}...")

        # 5. Append to Sheets
        row = [
            email_data['sender'],
            email_data['subject'],
            email_data['date'],
            email_data['body']
        ]
        
        result = append_to_sheet(sheets_service, SPREADSHEET_ID, row)
        
        if result:
            processed_count += 1
            message_ids_to_mark.append(msg['id'])

    # 6. Mark as Read
    if message_ids_to_mark:
        print("✅ Marking processed emails as read...")
        mark_as_read(gmail_service, message_ids_to_mark)

    # 7. Save State
    if messages:
        # Use the historyId from the most recent message (first in list usually)
        new_history_id = messages[0].get('historyId')
        if new_history_id:
            save_state(new_history_id)
            print(f"💾 State saved: historyId = {new_history_id}")

    # 8. Summary
    print(f"\n🎉 Done! Processed {processed_count} emails.")

if __name__ == '__main__':
    main()
