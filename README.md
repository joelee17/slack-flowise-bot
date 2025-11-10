# Slack Flowise Bot - Travel Card Assistant

A Slack bot that connects your Slack workspace to the Flowise Travel Card Agent, allowing users to provision travel cards directly through Slack.

## Features

- 📱 **Direct Messages**: Users can DM the bot directly
- 💬 **Channel Mentions**: Mention @TravelCardBot in any channel
- ⚡ **Slash Command**: Use `/travelcard` command
- 🔄 **Session Management**: Maintains conversation context per user
- 🏠 **App Home**: Beautiful home tab with instructions

## Setup Instructions

### 1. Create Slack App

1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name it "Travel Card Assistant" and select your workspace
4. Click "Create App"

### 2. Configure Bot Permissions

1. Go to **OAuth & Permissions**
2. Add these Bot Token Scopes:
   - `app_mentions:read` - Read messages that mention the bot
   - `chat:write` - Send messages
   - `im:history` - View messages in DMs
   - `im:read` - View basic info about DMs
   - `im:write` - Start DMs
   - `commands` - Add slash commands
   
3. Install the app to your workspace
4. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### 3. Enable Socket Mode

1. Go to **Socket Mode** in the sidebar
2. Enable Socket Mode
3. Create an **App-Level Token** with `connections:write` scope
4. Copy the **App-Level Token** (starts with `xapp-`)

### 4. Get Signing Secret

1. Go to **Basic Information**
2. Copy the **Signing Secret**

### 5. Configure Event Subscriptions

1. Go to **Event Subscriptions**
2. Enable Events
3. Subscribe to these **bot events**:
   - `app_mention` - When someone mentions the bot
   - `message.im` - Messages in DMs
   - `app_home_opened` - When user opens app home

### 6. Add Slash Command (Optional)

1. Go to **Slash Commands**
2. Click "Create New Command"
3. Command: `/travelcard`
4. Short Description: "Ask the Travel Card Assistant"
5. Usage Hint: "your question here"

### 7. Deploy to Render

1. Push this code to GitHub
2. Go to https://render.com
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `slack-flowise-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Instance Type**: Free or Starter

6. Add Environment Variables in Render:
   ```
   SLACK_BOT_TOKEN=xoxb-your-token
   SLACK_APP_TOKEN=xapp-your-token
   SLACK_SIGNING_SECRET=your-secret
   FLOWISE_URL=https://flowise-bwww.onrender.com/api/v1/prediction/376b207c-2027-47be-98c7-12f3d4e81c75
   ```

7. Click "Create Web Service"

### 8. Test Your Bot

1. Go to your Slack workspace
2. Find the bot in Apps
3. Send it a DM: "I need a travel card"
4. Or mention it in a channel: "@TravelCardBot help me with a travel card"
5. Or use the slash command: `/travelcard I need a card`

## Local Development

1. Clone the repository
2. Copy `env.example` to `.env` and fill in your tokens
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the bot:
   ```bash
   python app.py
   ```

## Architecture

```
Slack User → Slack Bot → Flowise API → Travel Card Agent
                ↓
         Session Management
         (per-user sessions)
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SLACK_BOT_TOKEN` | Bot User OAuth Token (xoxb-) | Yes |
| `SLACK_APP_TOKEN` | App-Level Token for Socket Mode (xapp-) | Yes |
| `SLACK_SIGNING_SECRET` | Signing secret from Basic Information | Yes |
| `FLOWISE_URL` | Flowise chatflow prediction endpoint | Yes |
| `PORT` | Port for health check (auto-set by Render) | No |

## Troubleshooting

### Bot doesn't respond
- Check that Socket Mode is enabled
- Verify all environment variables are set correctly
- Check Render logs for errors

### "Not authorized" error
- Make sure you've installed the app to your workspace
- Verify the Bot Token has the correct scopes

### Session not maintained
- Sessions are stored in memory per user
- If the bot restarts, sessions are reset
- For persistent sessions, add a database

## Support

For issues or questions, contact your workspace admin.

