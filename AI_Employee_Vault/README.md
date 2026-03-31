# AI Employee — Bronze Tier

## Setup
pip install -r requirements.txt

## Run Watcher (from inside AI_Employee_Vault/)
python filesystem_watcher.py

## Folder Structure
| Folder | Purpose |
|--------|---------|
| /Inbox | Drop zone for new files |
| /Needs_Action | Items awaiting review |
| /Done | Completed tasks |
| /Plans | Action plans |
| /Logs | JSON audit logs |
| /Pending_Approval | Awaiting human sign-off |
| /Approved | Approved for execution |
| /Skills | Agent Skill definitions |

## Bronze Tier Checklist
- [x] Dashboard.md
- [x] Company_Handbook.md
- [x] File System Watcher
- [x] Folder structure
- [x] Agent Skills in /Skills/
