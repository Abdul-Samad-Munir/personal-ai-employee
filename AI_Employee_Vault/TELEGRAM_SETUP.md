# Telegram Watcher Setup Guide

## Step 1: Create a Telegram Bot (2 minutes)
1. Open Telegram app
2. Search for @BotFather
3. Send: /newbot
4. Choose a name: e.g. "My AI Employee"
5. Choose a username: e.g. "myaiemployee_bot"
6. BotFather gives you a token like: 123456789:ABCdefGHI...
7. Copy that token

## Step 2: Add token to .env file
Inside AI_Employee_Vault/ create or edit .env:
TELEGRAM_BOT_TOKEN=your_token_here

## Step 3: Install dependency
pip install requests

## Step 4: Run the watcher
cd AI_Employee_Vault
python3 telegram_watcher.py

## Step 5: Test it
1. Open Telegram
2. Search for your bot username
3. Send it any message like "urgent invoice needed"
4. Check AI_Employee_Vault/Needs_Action/ — a .md file will appear
5. The bot will auto-reply: "Message received by AI Employee"

## How it works
- Bot uses official Telegram API (long polling)
- Every message is saved as .md file in /Needs_Action/
- Urgent keywords (invoice, payment, urgent, asap) get priority: high
- Bot sends automatic acknowledgement reply
- Full audit log written to /Logs/
