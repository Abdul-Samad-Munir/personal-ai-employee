---
skill_name: process_inbox
trigger: new file in /Inbox
version: 1.0
---

# Skill: Process Inbox

## Purpose
When a new file appears in /Inbox, analyze it and move it to the right location.

## Steps
1. Read the file content
2. Classify: is it an email, invoice, task, document, or unknown?
3. If it needs action → move to /Needs_Action/ with a metadata .md file
4. If it is FYI only → move to /Done/ directly
5. Update Dashboard.md with the new item
6. Log the action to /Logs/

## Output Format
Create a metadata .md file alongside the moved file:
---
type: [email/invoice/task/document]
source: inbox_drop
received: [datetime]
status: needs_action
priority: [high/medium/low]
---
## Summary
[1-2 line summary of what this file contains]
## Suggested Actions
- [ ] Action 1
- [ ] Action 2
