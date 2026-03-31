# LinkedIn Auto-Poster Setup Guide

## Step 1: Create a LinkedIn Developer App
1. Go to https://www.linkedin.com/developers/apps
2. Click "Create App"
3. Fill in:
   - App name: AI Employee
   - LinkedIn Page: your personal profile or company page
   - App logo: any image
4. Click Create

## Step 2: Get Permissions
1. Go to the "Products" tab
2. Request access to "Share on LinkedIn"
3. Go to "Auth" tab
4. Copy your Client ID and Client Secret

## Step 3: Get Access Token
1. Go to https://www.linkedin.com/developers/tools/oauth/token-generator
2. Select scopes: r_liteprofile, w_member_social
3. Click "Request access token"
4. Copy the token (valid for 60 days)

## Step 4: Get Your Person ID
Run this in terminal:
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.linkedin.com/v2/me

Copy the "id" field from the response.

## Step 5: Add to .env file
Create AI_Employee_Vault/.env:
LINKEDIN_ACCESS_TOKEN=your_token_here
LINKEDIN_PERSON_ID=your_person_id_here

## Step 6: Install dependency
pip install requests

## Step 7: Test
cd AI_Employee_Vault
python3 linkedin_poster.py --sample

This creates a post in /Pending_Approval/
Move it to /Approved/ to publish it to LinkedIn.

## Step 8: Run in watch mode
python3 linkedin_poster.py --watch
