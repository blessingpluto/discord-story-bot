# discord-story-bot

A Python bot that automatically monitors Instagram Stories from a specified profile, downloads them as soon as they are
published, and posts them directly to a Discord channel via webhook.

## Features

- Downloads new Instagram Stories automatically
- Avoids reposting stories already sent (using checksum tracking)
- Sends media files to Discord channels via webhook
- Runs on a schedule (default: every 10 minutes)
- Cleans up local downloaded files after sending to save space

## Requirements

- Python 3.7+

> ⚠️ **Note:**
> - You must have an existing Instagram account.
> - To download stories from private profiles, your account **must be following** those users.

## Installation

### 1. Clone this repository:

```bash
git clone https://github.com/yourusername/discord-story-bot.git
cd discord-story-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create an Instagram session file:

Run this once to login and save your session (replace your username):

```bash
instaloader --login=your_username
```

Follow Instagram login prompts and verify 2FA if necessary.

### 4. Configure config.py

Edit the config file with your Instagram username, your target username and Discord webhook URL.

## Usage

Start the bot with:

```bash
python bot.py
```

The bot will:

- Check for new stories every 10 minutes
- Download and send new stories to your Discord channel
- Delete local files after sending
- Keep track of already sent stories to avoid duplicates

## Customize

- Modify the schedule interval in config.py by changing STORY_DOWNLOAD_INTERVAL_MINUTES and
  CHECKSUM_CLEANUP_INTERVAL_MINUTES to your preferred time.
- Extend with logging or error handling as needed.

## Troubleshooting

If you encounter any issue while logging in or downloading stories (e.g., `KeyError: 'data'`), follow the steps below to
work around the login problem:

1. **Login to Instagram in Firefox.**
2. **Download the latest version of the Firefox session import script** from the official Instaloader GitHub repository:

    - Download the following
      script: https://raw.githubusercontent.com/instaloader/instaloader/master/docs/codesnippets/615_import_firefox_session.py
    - Save it to your project directory.

3. **Run the script** to import your Firefox session and create a valid session file for your Instagram account:
   ```bash
   python 615_import_firefox_session.py
   ```
4. Then instaloader **should work fine.**

> ⚠️ **Note:**  
> This script accesses your browser session data. Run it only in trusted environments.
> The script used in this project is sourced directly from the official Instaloader documentation, and should be kept up to date by checking the official source.

More info in the [official Instaloader documentation](https://instaloader.github.io/troubleshooting.html).
