---
skill_name: create_plan
trigger: new item appears in /Needs_Action
version: 1.0
---

# Skill: Create Plan

## Purpose
For every new item in /Needs_Action, create a structured Plan.md in /Plans/

## Steps
1. Read the item file
2. Identify the type: email, file, invoice, task
3. Create PLAN_[itemname].md in /Plans/ with:
   - Objective
   - Step by step checklist
   - Approval requirements
   - Notes
4. Log the plan creation to /Logs/
5. Update Dashboard.md

## Rules
- Every Needs_Action item must have a corresponding Plan
- Never execute without a plan
- If unsure what to do, flag for human review in /Pending_Approval/
