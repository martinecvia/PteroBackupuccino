from dataclasses import dataclass
from datetime import datetime

@dataclass
class Server:
    @dataclass
    class Backup:
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
    is_suspended: bool
    is_installing: bool

    backups: list[Backup] = []