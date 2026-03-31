# Gmail Watcher Setup Guide

## Step 1: Enable Gmail API
1. Go to https://console.cloud.google.com
2. Create a new project (or select existing)
3. Go to "APIs & Services" → "Enable APIs"
4. Search for "Gmail API" and enable it

## Step 2: Create Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client ID"
3. Application type: "Desktop App"
4. Download the JSON file
5. Rename it to credentials.json
6. Place it inside AI_Employee_Vault/

## Step 3: Install dependencies
pip install google-api-python-client google-auth-oauthlib

## Step 4: Run the watcher
cd AI_Employee_Vault
python3 gmail_watcher.py

## First run
A browser window will open asking you to log in to Google and grant permission.
After that, a token.json file is saved and the watcher runs automatically.

## Security Note
- Never commit credentials.json or token.json to GitHub
- Both files are already in .gitignore
