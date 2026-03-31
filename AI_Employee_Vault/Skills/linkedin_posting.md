---
skill_name: linkedin_posting
trigger: when business content needs to be posted on LinkedIn
version: 1.0
---

# Skill: LinkedIn Posting

## Purpose
Draft LinkedIn posts for human approval, then publish after approval.

## Steps
1. Generate post content based on business goals
2. Create approval file in /Pending_Approval/LINKEDIN_[timestamp].md
3. STOP — wait for human to move file to /Approved/
4. Once approved, publish via LinkedIn API
5. Log result and move to /Done/

## Post Guidelines
- Keep posts under 1300 characters
- Include relevant hashtags
- Professional but conversational tone
- End with a question or call to action

## Never Post Without Approval
LinkedIn posts are public and permanent.
Always require human review before publishing.
