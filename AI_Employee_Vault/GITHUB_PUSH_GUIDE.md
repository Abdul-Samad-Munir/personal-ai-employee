# GitHub Push Guide — Personal AI Employee

## What Is Safe to Commit
This repo uses .gitignore to block secrets. Before every push, verify:

| File | Safe? | Reason |
|------|-------|--------|
| *.py scripts | YES | No secrets inside |
| *.md files | YES | Documentation only |
| requirements.txt | YES | Package names only |
| scheduler.sh | YES | No secrets inside |
| .gitignore | YES | Should always be committed |
| credentials.json | NO | Google OAuth secret |
| token.json | NO | Live Google access token |
| .env | NO | Contains passwords |
| *.log | NO | May contain sensitive data |
| watcher.log | NO | Runtime log |
| __pycache__/ | NO | Python bytecode, not needed |

---

## One-Time Setup (do this once)

### 1. Create repo on GitHub
1. Go to https://github.com/new
2. Name it: `personal-ai-employee` (or your choice)
3. Set to Public or Private
4. Do NOT initialize with README (you already have one)
5. Click "Create repository"

### 2. Copy the remote URL shown on GitHub
It will look like:
```
https://github.com/YOUR_USERNAME/personal-ai-employee.git
```

---

## Git Commands to Push

Run these from inside `AI_Employee_Vault/` (or the Bronze folder if that's your root):

```bash
# Add GitHub as remote
git remote add origin https://github.com/YOUR_USERNAME/personal-ai-employee.git

# Verify remote was added
git remote -v

# Push to GitHub (first time)
git push -u origin main
```

If your default branch is called `master` instead of `main`:
```bash
git push -u origin master
```

---

## Every Future Push

```bash
git add .
git commit -m "describe what changed"
git push
```

---

## Security Checklist Before Every Push

Run this to confirm no secrets will be uploaded:

```bash
git status
```

Make sure you do NOT see any of these in the staged files:
- `credentials.json`
- `token.json`
- `.env`
- Any file with a real password or API key

If you accidentally staged a secret:
```bash
git reset HEAD credentials.json   # unstage it
```

---

## If You Accidentally Pushed a Secret

1. Revoke the credential immediately (Google Cloud Console → delete the OAuth key)
2. Remove from git history:
   ```bash
   git rm --cached credentials.json
   git commit -m "remove secret file"
   git push
   ```
3. Generate a new credential and start fresh

---

## Recommended .gitignore Additions

Your `.gitignore` already covers the main secrets. Double-check it includes:
```
.env
credentials.json
token.json
*.log
__pycache__/
*.pyc
.DS_Store
```
