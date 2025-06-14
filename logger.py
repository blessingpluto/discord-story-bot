import logging
import requests
from config import DISCORD_LOGS_WEBHOOK_URL, LOG_LEVEL, ENABLE_DISCORD_LOGS


def send_discord_log(content):
    try:
        requests.post(DISCORD_LOGS_WEBHOOK_URL, json={"content": content})
    except Exception:
        pass


class DiscordLogHandler(logging.Handler):
    def emit(self, record):
        msg = self.format(record)
        send_discord_log(f"```{msg}```")


LOGGING_LEVEL = getattr(logging, LOG_LEVEL)
LOGGING_FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

# Setup logger
logger = logging.getLogger("insta_bot")
logger.setLevel(LOGGING_LEVEL)

# Console output
console_handler = logging.StreamHandler()
console_handler.setLevel(LOGGING_LEVEL)  # mostra tutto in console
console_handler.setFormatter(LOGGING_FORMATTER)
logger.addHandler(console_handler)

# Discord logging
if ENABLE_DISCORD_LOGS:
    discord_handler = DiscordLogHandler()
    discord_handler.setLevel(LOGGING_LEVEL)
    discord_handler.setFormatter(LOGGING_FORMATTER)
    logger.addHandler(discord_handler)
