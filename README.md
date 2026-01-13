# Gmail to Sheets Automation

A Python script that scans your Gmail inbox for unread emails and appends them to a Google Sheet.

## Architecture

The project consists of three main components:
1. **Gmail Service**: Authenticates and fetches unread emails.
2. **Email Parser**: Extracts clean text (Sender, Subject, Date, Body) from raw MIME data.
3. **Sheets Service**: Appends the parsed data to a Google Sheet.

A local `state.json` file is used to persist the last processed `historyId`.

## Setup & OAuth Flow

This project uses **OAuth 2.0** for secure access to your Google account.

1. **Credentials**: You need a `credentials.json` file from the Google Cloud Console (OAuth 2.0 Client ID).
2. **First Run**: The script will open a browser window asking for permission.
3. **Token Storage**: After approval, a `token.json` file is created locally. This token is used for future runs so you don't have to log in every time.
4. **Scopes**:
   - `gmail.readonly`: To read emails.
   - `gmail.modify`: To remove the "UNREAD" label.
   - `spreadsheets`: To write to Google Sheets.

## Duplicate Prevention & State

We use two mechanisms to avoid duplicates:
1. **Search Query**: We only fetch emails matching `is:unread in:inbox`.
2. **State Persistence**: We save the Gmail `historyId` to `state.json` after every successful run.
   - **Why historyId?** It's a unique identifier for the state of your mailbox. While we currently rely on the "UNREAD" label, storing `historyId` allows for more robust syncing in the future (e.g., using `history.list` to find changes even if labels change).

## Challenges & Solutions

**Challenge**: Emails are complex MIME multipart structures (HTML, Plain Text, Attachments).
**Solution**: The `email_parser.py` specifically looks for the `text/plain` part of the payload. If not found, it falls back to the main body. This ensures we get readable text for the spreadsheet without HTML tags.

## Limitations

- **Local State**: `state.json` is stored locally. If you delete it or move environments, you might lose your sync checkpoint (though `is:unread` prevents re-reading old read emails).
- **No Attachments**: This script only extracts text content. Attachments are ignored.
- **Single Sheet**: Currently hardcoded to write to `Sheet1`.

## Usage

1. Place `credentials.json` in the `credentials/` folder.
2. Update `SPREADSHEET_ID` in `config.py`.
3. Run the script:
   ```bash
   python src/main.py
   ```

## Proof of Execution

### Demo Video
[Watch the Demo Video](https://drive.google.com/file/d/1H2ZAiVoZDkZmKTgMg0BOLu6fnrBFGZ5W/view?usp=sharing)
