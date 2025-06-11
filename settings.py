import logging
import sys

import argparse

class Settings:
    def __init__(self):
        arguments = self._arguments()
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("ptero_backup_backupuccino.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.PTERODACTYL_API_URL: str = arguments.PTERODACTYL_API_URL; self.PTERODACTYL_API_KEY = arguments.PTERODACTYL_API_KEY
        self.DISCORD_WEBHOOK_URL: str = arguments.DISCORD_WEBHOOK_URL

        self.HTTP_HEADER: str         = {
            "Authorization": f"Bearer {self.PTERODACTYL_API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        self.MAX_BACKUP_LIMIT: int    = arguments.MAX_BACKUP_LIMIT
        self.DELETE_LOCKED: bool = arguments.DELETE_LOCKED # If this is true
                                                           # locked backups will be included into backup list
                                                           # thus used towards backup limit
        self.APP_CHECK_INTERVAL: int = arguments.APP_CHECK_INTERVAL
        self.HTTP_TIMEOUT: int = arguments.HTTP_TIMEOUT; self.HTTP_RETRY_COUNT: int = arguments.HTTP_RETRY_COUNT; self.HTTP_RETRY_DELAY: int = arguments.HTTP_RETRY_DELAY

    def _arguments(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Basic arguments parser for Backupuccino")
        parser.add_argument("--PTERODACTYL_API_URL", required=True, help="Pterodactyl Client API URL")
        parser.add_argument("--PTERODACTYL_API_KEY", required=True, help="Pterodactyl Client API KEY")

        parser.add_argument("--DISCORD_WEBHOOK_URL", default="https://discord.com/api/webhooks/...", help="Discord webhook URL for notifications")
        parser.add_argument("--MAX_BACKUP_LIMIT", default=3, type=int); parser.add_argument("--DELETE_LOCKED", default=False, action="store_true")
        parser.add_argument("--APP_CHECK_INTERVAL", default=60*60*1, type=int)
        parser.add_argument("--HTTP_TIMEOUT", default=120, type=int); parser.add_argument("--HTTP_RETRY_COUNT", default=3, type=int); parser.add_argument("--HTTP_RETRY_DELAY", default=5, type=int)
        return parser.parse_args()