# Quick Deployment Guide

## Step 1: Set Up Your Environment Variables

You already have your Slack tokens. Create a `.env` file (copy from `env.example`):

```bash
cp env.example .env
```

Then edit `.env` and add your tokens:
- `SLACK_BOT_TOKEN` - Your Bot User OAuth Token
- `SLACK_APP_TOKEN` - Your App-Level Token for Socket Mode
- `SLACK_SIGNING_SECRET` - Your Signing Secret

## Step 2: Test Locally (Optional)

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the bot
python3 app.py
```

You should see: "Starting Slack bot..."

## Step 3: Deploy to Render

### Option A: Deploy via GitHub (Recommended)

1. Initialize git and push to GitHub:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Slack Flowise Bot"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/slack-flowise-bot.git
   git push -u origin main
   ```

2. Go to https://render.com/dashboard
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Render will auto-detect the `render.yaml` configuration
6. Add your environment variables:
   - `SLACK_BOT_TOKEN`
   - `SLACK_APP_TOKEN`
   - `SLACK_SIGNING_SECRET`
7. Click "Create Web Service"

### Option B: Deploy via Render Dashboard (Manual)

1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Choose "Public Git repository" and enter your repo URL
4. Configure:
   - **Name**: `slack-flowise-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Instance Type**: Free (or Starter for better performance)

5. Add Environment Variables:
   - `SLACK_BOT_TOKEN` = your bot token
   - `SLACK_APP_TOKEN` = your app token
   - `SLACK_SIGNING_SECRET` = your signing secret
   - `FLOWISE_URL` = `https://flowise-bwww.onrender.com/api/v1/prediction/376b207c-2027-47be-98c7-12f3d4e81c75`

6. Click "Create Web Service"

## Step 4: Verify Deployment

1. Wait for Render to build and deploy (2-3 minutes)
2. Check the logs in Render dashboard
3. You should see: "Starting Slack bot..."
4. The health check endpoint should be accessible at: `https://your-app.onrender.com/health`

## Step 5: Test in Slack

1. Go to your Slack workspace
2. Find the bot in the Apps section
3. Send it a DM: "Hello, I need help with a travel card"
4. Or mention it in a channel: "@TravelCardBot help"
5. Or use the slash command: `/travelcard I need a card`

## Troubleshooting

### Bot doesn't respond
- Check Render logs for errors
- Verify all environment variables are set
- Make sure Socket Mode is enabled in Slack app settings

### "Connection failed" error
- Check that `SLACK_APP_TOKEN` is correct and has `connections:write` scope
- Verify Socket Mode is enabled

### Bot responds but Flowise doesn't work
- Check that `FLOWISE_URL` is correct
- Test the Flowise endpoint directly with curl:
  ```bash
  curl -X POST https://flowise-bwww.onrender.com/api/v1/prediction/376b207c-2027-47be-98c7-12f3d4e81c75 \
    -H "Content-Type: application/json" \
    -d '{"question": "Hello"}'
  ```

## Next Steps

- Customize the bot's responses in `app.py`
- Add more slash commands
- Implement persistent session storage (database)
- Add analytics and logging
- Create custom Slack blocks for rich formatting

