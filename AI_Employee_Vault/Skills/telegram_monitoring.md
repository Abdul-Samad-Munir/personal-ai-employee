---
skill_name: telegram_monitoring
trigger: new message received by Telegram bot
version: 1.0
---

# Skill: Telegram Monitoring

## Purpose
Monitor Telegram bot for incoming messages and route them to Needs_Action.

## Steps
1. Receive message via Telegram Bot API
2. Check for urgent keywords: urgent, asap, invoice, payment, help
3. Save message as .md file in /Needs_Action/
4. Send auto-reply to sender confirming receipt
5. Log action to /Logs/
6. Orchestrator picks it up and creates a Plan

## Priority Rules
- Contains urgent keywords → priority: high
- Normal message → priority: medium
- Auto-reply always sent immediately
