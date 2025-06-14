# config.py

"""
Configuration file for discord-story-bot.

IMPORTANT:
You must configure the following variables with your own credentials:
- YOUR_USERNAME: Your Instagram username (must have an existing account).
- TARGET_USERNAME: The Instagram username from which to download stories.
- DISCORD_WEBHOOK_URL: The full URL of your Discord webhook to send stories to.
"""

YOUR_USERNAME = "your_username"
TARGET_USERNAME = "target_username"
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."

ENABLE_DISCORD_LOGS = False
DISCORD_LOGS_WEBHOOK_URL = "https://discord.com/api/webhooks/..."

DOWNLOAD_DIR = f"{TARGET_USERNAME}_stories"
SENT_FILE = "sent_stories.txt"

# Scheduling intervals
STORY_DOWNLOAD_INTERVAL_MINUTES = 5
CHECKSUM_CLEANUP_INTERVAL_MINUTES = 1440

LOG_LEVEL = "DEBUG"
