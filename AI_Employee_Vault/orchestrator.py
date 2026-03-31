#!/usr/bin/env python3
"""
Orchestrator — Silver Tier AI Employee
Scans Needs_Action/ and creates Plan.md files for each item
Also watches Approved/ folder and triggers actions
"""

import os
import json
import time
import logging
import subprocess
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

VAULT_PATH = Path('.')
NEEDS_ACTION = VAULT_PATH / 'Needs_Action'
PLANS = VAULT_PATH / 'Plans'
DONE = VAULT_PATH / 'Done'
LOGS = VAULT_PATH / 'Logs'
PENDING_APPROVAL = VAULT_PATH / 'Pending_Approval'
APPROVED = VAULT_PATH / 'Approved'

for folder in [NEEDS_ACTION, PLANS, DONE, LOGS, PENDING_APPROVAL, APPROVED]:
    folder.mkdir(parents=True, exist_ok=True)

processed_items = set()


def log_action(action_type, description, files, result='success'):
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = LOGS / f'{today}.json'
    entries = json.load(open(log_file)) if log_file.exists() else []
    entries.append({
        'timestamp': datetime.now().isoformat(),
        'action_type': action_type,
        'actor': 'orchestrator',
        'description': description,
        'files_affected': files,
        'approval_status': 'auto_approved',
        'result': result
    })
    json.dump(entries, open(log_file, 'w'), indent=2)


def create_plan(item_file: Path):
    """Create a Plan.md for a Needs_Action item"""
    content = item_file.read_text(encoding='utf-8')
    plan_path = PLANS / f'PLAN_{item_file.stem}.md'

    # Determine plan type based on file content
    item_type = 'unknown'
    if 'type: email' in content:
        item_type = 'email'
    elif 'type: file_drop' in content:
        item_type = 'file'
    elif 'type: invoice' in content:
        item_type = 'invoice'

    plan_content = f"""---
created: {datetime.now().isoformat()}
source_item: {item_file.name}
item_type: {item_type}
status: pending_approval
---

# Plan: {item_file.stem}

## Objective
Process {item_type} item: `{item_file.name}`

## Steps
- [x] Item detected in Needs_Action/
- [x] Plan created
- [ ] Review item content
- [ ] Determine required action
- [ ] Create approval request if needed (see /Pending_Approval/)
- [ ] Execute approved action
- [ ] Move to /Done/

## Item Summary
{content[:500]}

## Notes
- Created by Orchestrator at {datetime.now().strftime('%Y-%m-%d %H:%M')}
- Awaiting human review
"""
    plan_path.write_text(plan_content, encoding='utf-8')
    logger.info(f'Created plan: {plan_path.name}')
    log_action('plan_created', f'Plan created for {item_file.name}', [str(plan_path)])
    return plan_path


def check_approved_folder():
    """Check /Approved for items ready to execute"""
    for approved_file in APPROVED.glob('*.md'):
        if approved_file.name in processed_items:
            continue
        logger.info(f'Approved item found: {approved_file.name}')
        content = approved_file.read_text(encoding='utf-8')

        # Log the approval and mark as processed
        log_action('action_approved', f'Human approved: {approved_file.name}', [str(approved_file)])
        processed_items.add(approved_file.name)

        # Move to Done
        done_path = DONE / approved_file.name
        approved_file.rename(done_path)
        logger.info(f'Moved approved item to Done: {approved_file.name}')


def update_dashboard():
    """Update Dashboard.md with current state"""
    dashboard = VAULT_PATH / 'Dashboard.md'
    needs_action_files = list(NEEDS_ACTION.glob('*.md'))
    pending_files = list(PENDING_APPROVAL.glob('*.md'))
    done_today = [f for f in DONE.glob('*.md') if datetime.now().strftime('%Y-%m-%d') in f.stat().st_mtime.__str__()]

    needs_action_list = '\n'.join([f'- {f.name}' for f in needs_action_files]) or '- (none)'
    pending_list = '\n'.join([f'- {f.name}' for f in pending_files]) or '- (none)'

    dashboard_content = f"""---
last_updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
status: active
---

# AI Employee Dashboard

## Status Overview
| Area | Count | Status |
|------|-------|--------|
| Needs Action | {len(needs_action_files)} | {'⚠️ Items waiting' if needs_action_files else '✅ Clear'} |
| Pending Approval | {len(pending_files)} | {'⚠️ Needs your review' if pending_files else '✅ Clear'} |

## Needs Action
{needs_action_list}

## Pending Your Approval
{pending_list}

## Recently Completed
(check /Done folder)

## Alerts
{'⚠️ ' + str(len(needs_action_files)) + ' items need attention' if needs_action_files else '✅ All clear'}
"""
    dashboard.write_text(dashboard_content, encoding='utf-8')


def main():
    logger.info('Orchestrator STARTING')
    logger.info('Scanning Needs_Action/ every 30 seconds')

    while True:
        try:
            # Process new items in Needs_Action
            for item_file in NEEDS_ACTION.glob('*.md'):
                if item_file.name in processed_items:
                    continue

                logger.info(f'New item found: {item_file.name}')
                create_plan(item_file)
                processed_items.add(item_file.name)

            # Check approved folder
            check_approved_folder()

            # Update dashboard
            update_dashboard()

        except Exception as e:
            logger.error(f'Orchestrator error: {e}')

        time.sleep(30)


if __name__ == '__main__':
    main()
