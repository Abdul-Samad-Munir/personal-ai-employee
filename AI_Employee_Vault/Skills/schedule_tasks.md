---
skill_name: schedule_tasks
trigger: cron or manual
version: 1.0
---

# Skill: Schedule Tasks

## Purpose
Run recurring tasks on a schedule without human intervention.

## Scheduled Tasks
| Task | Frequency | Time |
|------|-----------|------|
| Scan Needs_Action | Every 30 min | Always |
| Update Dashboard | Every 30 min | Always |
| Check Approved folder | Every 30 min | Always |
| Daily summary | Daily | 8:00 AM |

## Steps
1. Orchestrator.py runs on schedule via cron
2. It scans all folders
3. Creates plans for new items
4. Updates dashboard
5. Logs all activity

## Setup
Run scheduler.sh to see cron installation instructions.
