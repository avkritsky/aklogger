from dataclasses import dataclass
from enum import Enum


class Level(Enum):
    """
    DEBUG = 4
    WARNING = 3
    INFO = 2
    CRITICAL = 1
    ERROR = 0
    """
    DEBUG = 4
    WARNING = 3
    INFO = 2
    CRITICAL = 1
    ERROR = 0


@dataclass(frozen=True)
class Record:
    user: str
    project: str
    ref: str
    level: int
    mess: str
