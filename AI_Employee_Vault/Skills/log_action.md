---
skill_name: log_action
trigger: after every AI action
version: 1.0
---

# Skill: Log Action

## Purpose
Create an audit trail of every AI action.

## Steps
1. Identify today's date for log filename: /Logs/YYYY-MM-DD.json
2. If log file doesn't exist, create it with an empty array []
3. Append a new JSON entry:
{
  "timestamp": "ISO datetime",
  "action_type": "file_moved/email_drafted/plan_created/etc",
  "actor": "claude_code",
  "description": "human readable description",
  "files_affected": ["list of file paths"],
  "approval_status": "auto_approved/pending/approved_by_human",
  "result": "success/failed/pending"
}
