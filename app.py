import asyncio
import logging

import aiohttp

from definitions import Server
from settings import Settings

from typing import Any, Literal

logger = logging.getLogger(__name__)

class Bootstrap:
    settings: Settings | None = None
    current_server_list: list[Server] = []

    async def request_with_retries(self, session: aiohttp.ClientSession, method: Literal["GET", "PUT", "POST", "DELETE", "PATCH"], url: str, **kwargs):
        for attempt in range(1, session.bootstrap.settings.HTTP_RETRY_COUNT + 1):
            try:
                async with session.request(method, f"{session.bootstrap.settings.PTERODACTYL_API_URL}{url}",
                                        headers=session.bootstrap.settings.HTTP_HEADER, timeout=session.bootstrap.settings.HTTP_TIMEOUT, **kwargs) as response:
                    if response.status == 200:
                        return await response.json(), response.status
                    elif response.status == 204:
                        return {}, response.status
            except Exception as exception:
                logger.warning(f"Attempt {attempt + 1}/{session.bootstrap.settings.HTTP_RETRY_COUNT} failed: {exception}")
                await asyncio.sleep(session.bootstrap.settings.HTTP_RETRY_DELAY)
                return None, exception
            logger.error(f"Maximum HTTP_RETRY_COUNT exceeded for {url}")
        return None, 401

async def try_authenticate(session: aiohttp.ClientSession) -> tuple[list[Server], Any]:
    try:
        manifest, last_result_info = await session.bootstrap.request_with_retries(session, "GET", "/")
        if not manifest:
            return [], last_result_info
        servers = []
        for server in manifest.get("data", []):
            attributes = server.get("attributes", {})
            servers.append(Server(
                identifier=attributes["identifier"],
                uuid=attributes["uuid"],
                name=attributes["name"],
                node={
                    "cs.dedicated0.node0": "wings0",
                    "cs.dedicated1.node0": "wings1",
                    "cs.dedicated2.node0": "wings2",
                }[attributes["node"]],
                is_suspended=bool(attributes["is_suspended"]),
                is_installing=bool(attributes["is_installing"]),
            ))
        return servers, last_result_info
    except Exception as exception:
        return [], exception

async def prune_backups_for_server(session: aiohttp.ClientSession, server: Server):
    backups, _ = await server.get_backups(session)
    if not backups or not server.is_active:
        return
    backups: list[Server.Backup] = backups
    backups.sort(key=lambda backup: backup.created_at, reverse=True)
    for backup in backups:
        if backup.is_successful == False:
            result, _ = await backup.delete(session)
            if result:
                logger.warning(f"Deleting: {backup.uuid}.zip with total size {backup.size / (1024 ** 3)} from: {backup.created_at}")
                backups.remove(backup)
    backups_for_deletion = (backups if session.bootstrap.settings.DELETE_LOCKED 
                            else [backup for backup in backups 
                                  if not backup.is_locked]) \
    [session.bootstrap.settings.MAX_BACKUP_LIMIT:]
    if not backups_for_deletion:
        return # No viable backups are ready for deletion
    for backup in backups_for_deletion:
        result, _ = await backup.delete(session)
        if result:
            logger.warning(f"Deleting: {backup.uuid}.zip with total size {backup.size / (1024 ** 3)} from: {backup.created_at}")
            # No need to remove backup from backups list, EOL

async def serve_forever(bootstrap: Bootstrap):
    async with aiohttp.ClientSession() as session:
        session.bootstrap = bootstrap # Necessary for transferring data between session and application
        while True:
            current_server_list, last_result_info = await try_authenticate(session)
            if last_result_info in [200, 204, 401]:
                if current_server_list:
                    bootstrap.current_server_list = current_server_list
                    tasks = [
                        prune_backups_for_server(session, server)
                        for server in current_server_list
                    ]
                    await asyncio.gather(*tasks)
                else: logger.warning(f"No servers were found using this key:{settings.PTERODACTYL_API_KEY[:16]}")
            else: logger.exception(f"Fatal error occurred with info:{last_result_info}")
            await asyncio.sleep(settings.APP_CHECK_INTERVAL)

if __name__ == "__main__":
    settings: Settings = Settings() # Load settings to memory of arguments list
    bootstrap = Bootstrap()
    bootstrap.settings = settings

    try:
        asyncio.run(serve_forever(bootstrap))
    except Exception as exception:
        logger.exception(f"Fatal error occurred: {exception}")
    except KeyboardInterrupt as _:
        logger.info("Bye !")