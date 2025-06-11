import logging
from typing import Literal
import aiohttp

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Server:
    """
    Represents a Pterodactyl server object with metadata its metadata
    Is used to obtain backups if not obtained already
    """

    @dataclass
    class Backup:
        """
        Represents a backup of the server.

        Attributes:
            server_identifier: (str): Unique identifier of the server.
            uuid (str): Unique identifier of the backup.
            name (str): Human-readable name of the backup.
            bytes (int): Size of the backup in bytes.
            created_at (datetime): When the backup was created.
            completed_at (datetime | None): When the backup completed, or None if still in progress.
        """
        server_identifier: str
        uuid: str
        name: str
        size: int

        created_at: datetime

        is_successful: bool
        is_locked: bool

        logger = logging.getLogger(__name__)

        async def delete(self, session: aiohttp.ClientSession):
            from app import Bootstrap
            bootstrap: Bootstrap = getattr(session, 'bootstrap', None)
            if not bootstrap:
                raise RuntimeError("Bootstrap is not attached to session !")
            url = f"/servers/{self.server_identifier}/backups/{self.uuid}"
            manifest, last_result_info = await bootstrap.request_with_retries(session, "DELETE", url)
            if last_result_info == 204:
                return True, last_result_info
            self.logger.warning(f"Failed to delete: {self.uuid}.zip, manifest: {manifest}")
            return False, last_result_info

    identifier: str | None
    uuid: str
    name: str
    """Display name of the server."""

    is_suspended: bool
    """Whether the server is currently suspended."""

    is_installing: bool
    """Whether the server is in the installation phase."""

    node: Literal["wings0", "wings1", "wings2"]

    logger = logging.getLogger(__name__)

    @property
    def is_active(self) -> bool:
        return not self.is_suspended and not self.is_installing

    async def get_backups(self, session: aiohttp.ClientSession):
        if self.is_suspended or self.is_installing:
            return [], 204
        from app import Bootstrap
        bootstrap: Bootstrap = getattr(session, 'bootstrap', None)
        if not bootstrap:
            raise RuntimeError("Bootstrap is not attached to session !")
        url = f"/servers/{self.identifier}/backups"
        try:
            manifest, last_result_info = await bootstrap.request_with_retries(session, "GET", url)
            if manifest is None:
                return [], last_result_info
            backups = []
            for backup in manifest.get("data", []):
                attributes = backup.get("attributes", {})
                backups.append(self.Backup(
                    server_identifier=self.identifier,
                    uuid=attributes["uuid"],
                    name=attributes["name"]  or attributes["uuid"],
                    size=attributes["bytes"] or 0,
                    created_at=datetime.fromisoformat(attributes["created_at"]),
                    is_successful=bool(attributes["is_successful"]),
                    is_locked=bool(attributes["is_locked"]),
                ))
            return backups, last_result_info
        except Exception as exception:
            return [], exception