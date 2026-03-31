#!/usr/bin/env python3
"""
Gmail Watcher — Silver Tier AI Employee
Monitors Gmail for important unread emails and saves them to /Needs_Action
"""

import os
import json
import time
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('gmail_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

VAULT_PATH = Path('.')
NEEDS_ACTION = VAULT_PATH / 'Needs_Action'
LOGS = VAULT_PATH / 'Logs'

for folder in [NEEDS_ACTION, LOGS]:
    folder.mkdir(parents=True, exist_ok=True)


def log_action(action_type, description, files, result='success'):
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = LOGS / f'{today}.json'
    entries = json.load(open(log_file)) if log_file.exists() else []
    entries.append({
        'timestamp': datetime.now().isoformat(),
        'action_type': action_type,
        'actor': 'gmail_watcher',
        'description': description,
        'files_affected': files,
        'approval_status': 'auto_approved',
        'result': result
    })
    json.dump(entries, open(log_file, 'w'), indent=2)


def create_email_action_file(message_id, sender, subject, snippet, priority='medium'):
    """Save email as a .md file in Needs_Action/"""
    safe_id = message_id[:12]
    filepath = NEEDS_ACTION / f'EMAIL_{safe_id}.md'
    content = f"""---
type: email
message_id: {message_id}
from: {sender}
subject: {subject}
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
---

## Email Summary
{snippet}

## Suggested Actions
- [ ] Read full email
- [ ] Reply if needed
- [ ] Move to /Done when complete
"""
    filepath.write_text(content, encoding='utf-8')
    logger.info(f'Created action file: {filepath.name}')
    log_action('email_captured', f'Email from {sender} saved to Needs_Action', [str(filepath)])
    return filepath


def run_gmail_watcher():
    """
    Gmail watcher using Google Gmail API.
    Requires credentials.json from Google Cloud Console.
    Run setup first: python3 gmail_setup.py
    """
    try:
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build

        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        creds = None
        token_path = Path('token.json')
        creds_path = Path('credentials.json')

        if not creds_path.exists():
            logger.error('credentials.json not found. See GMAIL_SETUP.md for instructions.')
            return

        if token_path.exists():
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_path), SCOPES)
            creds = flow.run_local_server(port=0)
            token_path.write_text(creds.to_json())

        service = build('gmail', 'v1', credentials=creds)
        processed_ids = set()

        logger.info('Gmail Watcher STARTING — checking every 2 minutes')

        while True:
            try:
                results = service.users().messages().list(
                    userId='me',
                    q='is:unread is:important',
                    maxResults=10
                ).execute()

                messages = results.get('messages', [])

                for msg in messages:
                    if msg['id'] in processed_ids:
                        continue

                    full_msg = service.users().messages().get(
                        userId='me', id=msg['id']
                    ).execute()

                    headers = {h['name']: h['value'] for h in full_msg['payload']['headers']}
                    sender = headers.get('From', 'Unknown')
                    subject = headers.get('Subject', 'No Subject')
                    snippet = full_msg.get('snippet', '')

                    # Flag high priority keywords
                    priority = 'high' if any(k in subject.lower() for k in ['urgent', 'invoice', 'payment', 'asap']) else 'medium'

                    create_email_action_file(msg['id'], sender, subject, snippet, priority)
                    processed_ids.add(msg['id'])

                time.sleep(120)  # Check every 2 minutes

            except Exception as e:
                logger.error(f'Gmail check failed: {e}')
                time.sleep(60)

    except ImportError:
        logger.error('Google API libraries not installed. Run: pip install google-api-python-client google-auth-oauthlib')


if __name__ == '__main__':
    run_gmail_watcher()
