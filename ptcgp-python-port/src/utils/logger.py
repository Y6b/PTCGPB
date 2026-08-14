import logging
import requests
import json
from datetime import datetime

class BotLogger:
    def __init__(self, name="PTCGP_Bot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        if not self.logger.handlers:
            self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger

    def log_to_discord(self, webhook_url, message, username="PTCGP Bot"):
        """Sends a simple message to a Discord webhook."""
        if not webhook_url:
            self.logger.warning("No Discord webhook URL provided.")
            return False

        data = {
            "content": message,
            "username": username
        }

        try:
            response = requests.post(
                webhook_url,
                data=json.dumps(data),
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            self.logger.debug("Successfully sent message to Discord.")
            return True
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to send message to Discord: {e}")
            return False

# Default instance for convenient imports
bot_logger = BotLogger()
logger = bot_logger.get_logger()
