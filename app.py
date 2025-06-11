import asyncio
import logging

import aiohttp

from definitions import Server
from settings import Settings

logger = logging.getLogger(__name__)

class Bootstrap:
    settings: Settings | None = None
    current_server_list: list[Server] = []

async def try_authenticate(session: aiohttp.ClientSession):
    try:
        ...
    except Exception as exception:
        return [], exception

async def serve_forever(bootstrap: Bootstrap):
    async with aiohttp.ClientSession() as session:
        while True:
            current_server_list, last_result_info = await try_authenticate(session)
            if last_result_info == 200:
                if current_server_list:
                    bootstrap.current_server_list = current_server_list
                else: logger.warning(f"No servers were found using this key:{settings.PTERODACTYL_API_KEY[:16]}")
            else: logger.exception(f"Fatal error occurred: {exception}")
            await asyncio.sleep(settings.APP_CHECK_INTERVAL)
            
if __name__ == "__main__":
    settings: Settings = Settings() # Load settings to memory of arguments list
    bootstrap = Bootstrap()
    bootstrap.settings = settings

    try:
        asyncio.run(serve_forever(bootstrap))
    except Exception as exception:
        logging.exception(f"Fatal error occurred: {exception}")