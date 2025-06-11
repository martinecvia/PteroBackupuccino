from dataclasses import dataclass, field
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
            uuid (str): Unique identifier of the backup.
            name (str): Human-readable name of the backup.
            bytes (int): Size of the backup in bytes.
            created_at (datetime): When the backup was created.
            completed_at (datetime | None): When the backup completed, or None if still in progress.
        """
        uuid: str
        name: str
        bytes: int
        created_at: datetime
        completed_at: datetime | None

        def is_locked(self) -> bool:
            return False
        
    identifier: str | None
    uuid: str
    name: str
    """Display name of the server."""

    is_suspended: bool
    """Whether the server is currently suspended."""

    is_installing: bool
    """Whether the server is in the installation phase."""

    backups: list[Backup] = field(default_factory=list)
    """List of backups associated with the server."""