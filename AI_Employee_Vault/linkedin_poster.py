#!/usr/bin/env python3
"""
LinkedIn Auto-Poster — Silver Tier AI Employee
Posts content to LinkedIn automatically with human approval
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
        logging.FileHandler('linkedin.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

VAULT_PATH = Path('.')
PENDING_APPROVAL = VAULT_PATH / 'Pending_Approval'
APPROVED = VAULT_PATH / 'Approved'
DONE = VAULT_PATH / 'Done'
LOGS = VAULT_PATH / 'Logs'

for folder in [PENDING_APPROVAL, APPROVED, DONE, LOGS]:
    folder.mkdir(parents=True, exist_ok=True)


def log_action(action_type, description, files, result='success'):
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = LOGS / f'{today}.json'
    entries = json.load(open(log_file)) if log_file.exists() else []
    entries.append({
        'timestamp': datetime.now().isoformat(),
        'action_type': action_type,
        'actor': 'linkedin_poster',
        'description': description,
        'files_affected': files,
        'approval_status': 'pending_human',
        'result': result
    })
    json.dump(entries, open(log_file, 'w'), indent=2)


def draft_linkedin_post(content: str, reason: str = ''):
    """
    Create approval request for LinkedIn post.
    Human must move file to /Approved to actually post.
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    approval_file = PENDING_APPROVAL / f'LINKEDIN_{timestamp}.md'

    approval_content = f"""---
type: approval_request
action: linkedin_post
created: {datetime.now().isoformat()}
status: pending
---

## LinkedIn Post to Publish

{content}

---
**Reason:** {reason}

## To Approve
Move this file to /Approved — post will be published automatically.

## To Reject
Move this file to /Done — post will NOT be published.
"""
    approval_file.write_text(approval_content, encoding='utf-8')
    logger.info(f'LinkedIn approval request created: {approval_file.name}')
    log_action('linkedin_draft_created', f'LinkedIn post queued for approval', [str(approval_file)])
    return approval_file


def post_to_linkedin(content: str):
    """
    Post to LinkedIn using LinkedIn API v2.
    Requires LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_ID in environment.
    """
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    person_id = os.getenv('LINKEDIN_PERSON_ID')

    if not access_token or not person_id:
        logger.error('LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_ID not set in .env')
        logger.info('See LINKEDIN_SETUP.md for instructions')
        return False

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    post_data = {
        'author': f'urn:li:person:{person_id}',
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {
                    'text': content
                },
                'shareMediaCategory': 'NONE'
            }
        },
        'visibility': {
            'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
        }
    }

    try:
        response = requests.post(
            'https://api.linkedin.com/v2/ugcPosts',
            headers=headers,
            json=post_data
        )

        if response.status_code == 201:
            logger.info('LinkedIn post published successfully!')
            log_action('linkedin_posted', 'Post published to LinkedIn', [], 'success')
            return True
        else:
            logger.error(f'LinkedIn API error: {response.status_code} — {response.text}')
            log_action('linkedin_posted', f'Failed: {response.status_code}', [], 'failed')
            return False

    except Exception as e:
        logger.error(f'LinkedIn post failed: {e}')
        return False


def watch_approved_folder():
    """Watch /Approved for LinkedIn post approvals and publish them."""
    logger.info('Watching /Approved for LinkedIn posts...')
    processed = set()

    while True:
        for approved_file in APPROVED.glob('LINKEDIN_*.md'):
            if approved_file.name in processed:
                continue

            logger.info(f'Approved LinkedIn post found: {approved_file.name}')
            content = approved_file.read_text(encoding='utf-8')

            # Extract post content (between ## LinkedIn Post to Publish and ---)
            start = content.find('## LinkedIn Post to Publish\n') + len('## LinkedIn Post to Publish\n')
            end = content.find('\n---\n', start)
            post_text = content[start:end].strip()

            if post_text:
                success = post_to_linkedin(post_text)
                if success:
                    done_path = DONE / approved_file.name
                    approved_file.rename(done_path)
                    processed.add(approved_file.name)
                    logger.info('Post published and moved to Done/')
            else:
                logger.warning('No post content found in approval file')

        time.sleep(30)


def generate_sample_post():
    """Generate a sample business post for approval."""
    sample_posts = [
        """🤖 Just built my Personal AI Employee using Claude Code!

It monitors my inbox 24/7, creates action plans automatically, and never takes sensitive actions without my approval.

The future of productivity is human-in-the-loop AI automation.

#AI #Productivity #ClaudeCode #Automation #Pakistan""",

        """💡 Did you know? A Digital AI Employee works 8,760 hours/year vs a human's 2,000.

Cost per task drops from $5 to $0.50 — that's 90% savings.

I just built one. Here's what it does:
✅ Monitors Gmail 24/7
✅ Creates action plans automatically
✅ Requires human approval for sensitive actions
✅ Full audit trail of every action

#DigitalTransformation #AI #Automation #PIAIC""",
    ]

    import random
    return random.choice(sample_posts)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--watch':
        # Watch mode: monitor Approved/ and post approved content
        watch_approved_folder()
    elif len(sys.argv) > 1 and sys.argv[1] == '--sample':
        # Generate a sample post for approval
        post_content = generate_sample_post()
        approval_file = draft_linkedin_post(post_content, 'Auto-generated sample post')
        print(f'Sample post created for approval: {approval_file}')
        print('Move it to /Approved to publish, or /Done to reject.')
    else:
        # Default: create a sample approval request
        post_content = generate_sample_post()
        approval_file = draft_linkedin_post(post_content, 'Sample post for testing')
        print(f'Approval request created: {approval_file.name}')
        print('Review it in /Pending_Approval/ then move to /Approved to post.')
