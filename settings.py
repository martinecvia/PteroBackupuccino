import logging
import sys

class Settings:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("ptero_backup_backupuccino.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def _is_init(self) -> bool:
        return all([
                self.PTERODACTYL_API_URL != "https://panel.example.com", 
                self.PTERODACTYL_APPLICATION_KEY != "your_api_key_here", 
                self.PTERODACTYL_CLIENT_KEY != "your_api_key_here"
            ])

    PTERODACTYL_API_URL = "https://panel.example.com"
    PTERODACTYL_APPLICATION_KEY = "your_api_key_here"
    PTERODACTYL_CLIENT_KEY = "your_api_key_here"
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."

    MAX_BACKUP_LIMIT    = 3
    USE_LOCKED_BACKUPS  = False # If this is true
                                # locked backups will be included into backup list
                                # thus used towards backup limit
    DELETE_LOCKED       = False # Only usable if {{USE_LOCKED_BACKUPS}} is True

    HTTP_TIMEOUT        = 10
    HTTP_RETRY_COUNT    = 3
    HTTP_RETRY_DELAY    = 3
    HTTP_HEADER         = {
        "Authorization": "Bearer %Key",
        "Accept": "Application/vnd.pterodactyl.v1+json",
        "Content-Type": "application/json"
    }

    APP_CHECK_INTERVAL  = 60 * 60 * 1 # Every hour application should start and check

