---
skill_name: human_in_the_loop
trigger: before any sensitive action
version: 1.0
---

# Skill: Human in the Loop

## Purpose
Before taking any sensitive action, create an approval request file and WAIT.

## Sensitive Actions (always require approval)
- Sending any email
- Making any payment
- Posting on social media
- Deleting any file
- Contacting new recipients

## Steps
1. Create an approval file in /Pending_Approval/ with full details
2. Stop — do NOT proceed
3. Wait for human to move file to /Approved/
4. Only then execute the action
5. Log the result

## Approval File Format
---
type: approval_request
action: [what you want to do]
created: [datetime]
status: pending
---
## Details
[Full description of what will happen]
## To Approve
Move this file to /Approved/
## To Reject
Move this file to /Done/
