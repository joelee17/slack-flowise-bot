"""
Slack Bot for Flowise Credit Card Agent
Connects Slack workspace to Flowise chatflow for travel card provisioning
"""

import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Slack app with tokens from environment variables
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Flowise configuration
FLOWISE_URL = os.environ.get("FLOWISE_URL", "https://flowise-bwww.onrender.com/api/v1/prediction/376b207c-2027-47be-98c7-12f3d4e81c75")

# Store user sessions (Slack user ID -> Flowise session ID)
user_sessions = {}

def get_flowise_session_id(slack_user_id):
    """Get or create a Flowise session ID for a Slack user"""
    if slack_user_id not in user_sessions:
        # Create a new session ID for this user
        user_sessions[slack_user_id] = f"slack-{slack_user_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    return user_sessions[slack_user_id]

def chat_with_flowise(message, slack_user_id):
    """Send message to Flowise and get response"""
    try:
        session_id = get_flowise_session_id(slack_user_id)
        
        payload = {
            "question": message,
            "overrideConfig": {
                "sessionId": session_id
            }
        }
        
        logger.info(f"Sending to Flowise: user={slack_user_id}, session={session_id}, message_length={len(message)}")
        
        response = requests.post(
            FLOWISE_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        logger.info(f"Flowise response: status={response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict):
                flowise_response = result.get('text', result.get('output', result.get('answer', str(result))))
                logger.info(f"Response length: {len(flowise_response) if flowise_response else 0}")
                return flowise_response
            else:
                return str(result)
        else:
            error_msg = f"Error: HTTP {response.status_code} from Flowise"
            logger.error(f"Flowise error: {error_msg}")
            return f"Sorry, I encountered an error connecting to the travel card service. Please try again."
            
    except Exception as e:
        error_msg = f"Error communicating with Flowise: {str(e)}"
        logger.error(error_msg)
        return f"Sorry, I encountered an error: {str(e)}"

# Handle app mentions (@bot_name)
@app.event("app_mention")
def handle_app_mention(event, say, logger):
    """Handle when the bot is mentioned in a channel"""
    user_id = event["user"]
    text = event["text"]
    
    # Remove the bot mention from the text
    # Slack mentions look like <@U12345678>
    import re
    clean_text = re.sub(r'<@[A-Z0-9]+>', '', text).strip()
    
    if not clean_text:
        say(
            text="Hi! I'm the Travel Card Assistant. Ask me anything about provisioning travel cards!",
            thread_ts=event.get("thread_ts", event["ts"])
        )
        return
    
    logger.info(f"App mention from user {user_id}: {clean_text}")
    
    # Get response from Flowise
    response = chat_with_flowise(clean_text, user_id)
    
    # Reply in thread if the message was in a thread, otherwise reply normally
    say(
        text=response,
        thread_ts=event.get("thread_ts", event["ts"])
    )

# Handle direct messages
@app.event("message")
def handle_message(event, say, logger):
    """Handle direct messages to the bot"""
    # Ignore bot messages and messages with subtypes (like message_changed)
    if event.get("subtype") or event.get("bot_id"):
        return
    
    # Only handle direct messages (DMs)
    channel_type = event.get("channel_type")
    if channel_type != "im":
        return
    
    user_id = event["user"]
    text = event["text"]
    
    logger.info(f"DM from user {user_id}: {text}")
    
    # Get response from Flowise
    response = chat_with_flowise(text, user_id)
    
    # Reply to the user
    say(text=response)

# Handle slash command (optional)
@app.command("/travelcard")
def handle_travelcard_command(ack, command, say, logger):
    """Handle /travelcard slash command"""
    ack()
    
    user_id = command["user_id"]
    text = command.get("text", "")
    
    if not text:
        say("Hi! Ask me anything about provisioning travel cards. For example: 'I need a travel card for John Doe'")
        return
    
    logger.info(f"Slash command from user {user_id}: {text}")
    
    # Get response from Flowise
    response = chat_with_flowise(text, user_id)
    
    # Reply to the user
    say(response)

# Handle app home opened (optional - shows a nice home tab)
@app.event("app_home_opened")
def handle_app_home_opened(event, client, logger):
    """Handle when user opens the app home tab"""
    user_id = event["user"]
    
    try:
        client.views_publish(
            user_id=user_id,
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome to the Travel Card Assistant! 🎫*\n\nI can help you provision travel cards for your employees."
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*How to use me:*\n• Send me a direct message\n• Mention me in a channel with @TravelCardBot\n• Use the `/travelcard` command"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Example questions:*\n• 'I need a travel card for John Doe'\n• 'How do I provision a card?'\n• 'What's the status of my request?'"
                        }
                    }
                ]
            }
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

# Health check endpoint for Render
from flask import Flask, jsonify
flask_app = Flask(__name__)

@flask_app.route('/health')
def health_check():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@flask_app.route('/')
def home():
    """Root endpoint"""
    return jsonify({
        "app": "Slack Flowise Bot",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    })

# Start the app
if __name__ == "__main__":
    # Check for required environment variables
    required_vars = ["SLACK_BOT_TOKEN", "SLACK_APP_TOKEN", "SLACK_SIGNING_SECRET"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        exit(1)
    
    logger.info("Starting Slack bot...")
    logger.info(f"Flowise URL: {FLOWISE_URL}")
    
    # Start Flask app in a separate thread for health checks
    import threading
    flask_thread = threading.Thread(
        target=lambda: flask_app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
    )
    flask_thread.daemon = True
    flask_thread.start()
    
    # Start the Slack bot with Socket Mode
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()

