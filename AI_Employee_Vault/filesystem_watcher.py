#!/usr/bin/env python3
"""
File System Watcher — Bronze Tier AI Employee
Monitors /Inbox folder and moves new files to /Needs_Action
"""

import time
import shutil
import logging
import json
from datetime import datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

VAULT_PATH = Path('.')
INBOX = VAULT_PATH / 'Inbox'
NEEDS_ACTION = VAULT_PATH / 'Needs_Action'
DONE = VAULT_PATH / 'Done'
LOGS = VAULT_PATH / 'Logs'

for folder in [INBOX, NEEDS_ACTION, DONE, LOGS]:
    folder.mkdir(parents=True, exist_ok=True)


def log_action(action_type, description, files, result='success'):
    today = datetime.now().strftime('%Y-%m-%d')
    log_file = LOGS / f'{today}.json'
    entries = json.load(open(log_file)) if log_file.exists() else []
    entries.append({
        'timestamp': datetime.now().isoformat(),
        'action_type': action_type,
        'actor': 'filesystem_watcher',
        'description': description,
        'files_affected': files,
        'approval_status': 'auto_approved',
        'result': result
    })
    json.dump(entries, open(log_file, 'w'), indent=2)


def create_metadata(source_file, dest_file):
    meta_path = NEEDS_ACTION / f'{source_file.stem}_meta.md'
    meta_path.write_text(f"""---
type: file_drop
original_name: {source_file.name}
received: {datetime.now().isoformat()}
status: needs_action
priority: medium
---

## Summary
New file dropped into Inbox: `{source_file.name}`

## Suggested Actions
- [ ] Review file content
- [ ] Classify and process
- [ ] Move to /Done when complete
""", encoding='utf-8')
    return meta_path


class InboxHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        source = Path(event.src_path)
        if source.name.startswith('.') or source.name.startswith('~'):
            return
        time.sleep(0.5)
        logger.info(f'New file detected: {source.name}')
        dest = NEEDS_ACTION / source.name
        if dest.exists():
            ts = datetime.now().strftime('%H%M%S')
            dest = NEEDS_ACTION / f'{source.stem}_{ts}{source.suffix}'
        try:
            shutil.move(str(source), str(dest))
            logger.info(f'Moved {source.name} to Needs_Action/')
            create_metadata(source, dest)
            log_action('file_moved', f'{source.name} moved from Inbox to Needs_Action', [str(source), str(dest)])
        except Exception as e:
            logger.error(f'Failed: {e}')
            log_action('file_moved', f'Failed to move {source.name}: {e}', [str(source)], 'failed')


def main():
    logger.info('AI Employee File Watcher STARTING')
    logger.info(f'Watching: {INBOX.resolve()}')
    observer = Observer()
    observer.schedule(InboxHandler(), str(INBOX), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
