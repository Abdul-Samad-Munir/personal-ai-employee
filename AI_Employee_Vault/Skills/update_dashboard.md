---
skill_name: update_dashboard
trigger: after any task completion or new item arrival
version: 1.0
---

# Skill: Update Dashboard

## Purpose
Keep Dashboard.md always current and accurate.

## Steps
1. Read all files in /Needs_Action/
2. Read all files in /Pending_Approval/
3. Read all files added to /Done/ today
4. Rewrite the relevant sections of Dashboard.md
5. Add timestamp to last_updated field

## Rules
- Keep the dashboard under 100 lines for readability
- Flag anything older than 48 hours in Needs_Action as OVERDUE
