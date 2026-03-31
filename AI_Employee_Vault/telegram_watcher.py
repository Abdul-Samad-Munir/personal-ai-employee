#!/usr/bin/env python3
"""
Telegram Watcher — Silver Tier AI Employee
Monitors a Telegram bot for messages and saves urgent ones to /Needs_Action
Uses official Telegram Bot API — no terms of service issues
"""

import os
import json
import time
import logging
import requests
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('telegram_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

VAULT_PATH = Path('.')
NEEDS_ACTION = VAULT_PATH / 'Needs_Action'
LOGS = VAULT_PATH / 'Logs'

for folder in [NEEDS_ACTION, LOGS]:
    folder.mkdir(parents=True, exist_ok=True)

# Keywords that trigger action file creation
URGENT_KEYWORDS = [
    'urgent', 'asap', 'invoice', 'payment', 'help',
    'important', 'deadline', 'meeting', 'call', 'issue'
]


def log_action(action_type, description, files, result='success'):
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = LOGS / f'{today}.json'
    entries = json.load(open(log_file)) if log_file.exists() else []
    entries.append({
        'timestamp': datetime.now().isoformat(),
        'action_type': action_type,
        'actor': 'telegram_watcher',
        'description': description,
        'files_affected': files,
        'approval_status': 'auto_approved',
        'result': result
    })
    json.dump(entries, open(log_file, 'w'), indent=2)


def create_telegram_action_file(message: dict):
    """Save Telegram message as .md file in Needs_Action/"""
    msg_id = message.get('message_id', 'unknown')
    chat = message.get('chat', {})
    sender = message.get('from', {})
    text = message.get('text', '')

    chat_name = chat.get('title') or chat.get('username') or chat.get('first_name', 'Unknown')
    sender_name = sender.get('first_name', '') + ' ' + sender.get('last_name', '')
    sender_name = sender_name.strip() or 'Unknown'

    # Determine priority
    priority = 'high' if any(kw in text.lower() for kw in URGENT_KEYWORDS) else 'medium'

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = NEEDS_ACTION / f'TELEGRAM_{timestamp}_{msg_id}.md'

    content = f"""---
type: telegram_message
message_id: {msg_id}
from: {sender_name}
chat: {chat_name}
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
---

## Message Content
{text}

## Suggested Actions
- [ ] Review message
- [ ] Reply if needed
- [ ] Move to /Done when complete
"""
    filepath.write_text(content, encoding='utf-8')
    logger.info(f'Telegram message saved: {filepath.name}')
    log_action('telegram_message_captured', f'Message from {sender_name} in {chat_name}', [str(filepath)])
    return filepath


def send_telegram_reply(bot_token: str, chat_id: int, text: str):
    """Send a reply via Telegram bot."""
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    try:
        response = requests.post(url, json={'chat_id': chat_id, 'text': text})
        return response.json().get('ok', False)
    except Exception as e:
        logger.error(f'Failed to send reply: {e}')
        return False


def run_telegram_watcher():
    """
    Main watcher loop using Telegram Bot API long polling.
    Requires TELEGRAM_BOT_TOKEN in environment.
    """
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not bot_token:
        logger.error('TELEGRAM_BOT_TOKEN not set. See TELEGRAM_SETUP.md')
        return

    base_url = f'https://api.telegram.org/bot{bot_token}'
    offset = 0
    logger.info('Telegram Watcher STARTING')
    logger.info('Waiting for messages...')

    # Send auto-reply template
    AUTO_REPLY = "✅ Message received by AI Employee. Will be reviewed shortly."

    while True:
        try:
            # Long polling — waits up to 30 seconds for new messages
            response = requests.get(
                f'{base_url}/getUpdates',
                params={'offset': offset, 'timeout': 30},
                timeout=35
            )
            data = response.json()

            if not data.get('ok'):
                logger.error(f'Telegram API error: {data}')
                time.sleep(10)
                continue

            updates = data.get('result', [])

            for update in updates:
                offset = update['update_id'] + 1
                message = update.get('message')

                if not message or 'text' not in message:
                    continue

                text = message.get('text', '')
                chat_id = message['chat']['id']
                sender = message.get('from', {}).get('first_name', 'Someone')

                logger.info(f'New message from {sender}: {text[:50]}')

                # Save to Needs_Action
                create_telegram_action_file(message)

                # Send auto-reply
                send_telegram_reply(bot_token, chat_id, AUTO_REPLY)

        except requests.exceptions.Timeout:
            # Normal — long polling timeout, just continue
            continue
        except Exception as e:
            logger.error(f'Watcher error: {e}')
            time.sleep(10)


if __name__ == '__main__':
    run_telegram_watcher()
