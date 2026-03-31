#!/usr/bin/env python3
"""
Email MCP Server — Silver Tier AI Employee
Handles email drafting and sending with human approval
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VAULT_PATH = Path('.')
PENDING_APPROVAL = VAULT_PATH / 'Pending_Approval'
LOGS = VAULT_PATH / 'Logs'

PENDING_APPROVAL.mkdir(parents=True, exist_ok=True)


def log_action(action_type, description, files, result='success'):
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = LOGS / f'{today}.json'
    entries = json.load(open(log_file)) if log_file.exists() else []
    entries.append({
        'timestamp': datetime.now().isoformat(),
        'action_type': action_type,
        'actor': 'email_mcp_server',
        'description': description,
        'files_affected': files,
        'approval_status': 'pending_human',
        'result': result
    })
    json.dump(entries, open(log_file, 'w'), indent=2)


def draft_email_approval(to: str, subject: str, body: str, reason: str = ''):
    """
    Instead of sending directly, create an approval request file.
    Human must move file to /Approved to trigger actual send.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    approval_file = PENDING_APPROVAL / f'EMAIL_{timestamp}.md'

    content = f"""---
type: approval_request
action: send_email
to: {to}
subject: {subject}
created: {datetime.now().isoformat()}
expires: (24 hours from creation)
status: pending
---

## Email to Send

**To:** {to}
**Subject:** {subject}

**Body:**
{body}

**Reason for sending:** {reason}

## To Approve
Move this file to /Approved folder — email will be sent automatically.

## To Reject
Move this file to /Done folder — email will NOT be sent.
"""
    approval_file.write_text(content, encoding='utf-8')
    logger.info(f'Email approval request created: {approval_file.name}')
    log_action('email_approval_requested', f'Email to {to} queued for approval', [str(approval_file)])
    return approval_file


def send_email_if_approved(approved_file: Path):
    """
    Called when human moves file to /Approved.
    Reads the approval file and sends the email.
    Requires EMAIL_ADDRESS and EMAIL_PASSWORD in environment variables.
    """
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    content = approved_file.read_text(encoding='utf-8')

    # Parse fields from markdown frontmatter
    lines = content.split('\n')
    to_email = next((l.replace('to:', '').strip() for l in lines if l.startswith('to:')), None)
    subject = next((l.replace('subject:', '').strip() for l in lines if l.startswith('subject:')), None)

    # Get body (after ## Email to Send section)
    body_start = content.find('**Body:**')
    body_end = content.find('**Reason')
    body = content[body_start+9:body_end].strip() if body_start > 0 else ''

    sender_email = os.getenv('EMAIL_ADDRESS')
    sender_password = os.getenv('EMAIL_PASSWORD')

    if not sender_email or not sender_password:
        logger.error('EMAIL_ADDRESS and EMAIL_PASSWORD not set in environment')
        return False

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)

        logger.info(f'Email sent to {to_email}')
        log_action('email_sent', f'Email sent to {to_email}', [str(approved_file)], 'success')
        return True

    except Exception as e:
        logger.error(f'Failed to send email: {e}')
        log_action('email_sent', f'Failed to send email: {e}', [str(approved_file)], 'failed')
        return False


if __name__ == '__main__':
    # Demo: create a sample approval request
    draft_email_approval(
        to='client@example.com',
        subject='Invoice for January 2026',
        body='Dear Client,\n\nPlease find attached your invoice for January 2026.\n\nBest regards',
        reason='Client requested invoice via WhatsApp'
    )
    print('Sample approval request created in /Pending_Approval/')
