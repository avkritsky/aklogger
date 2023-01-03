import json

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

    @property
    def rebytes(self):
        return bytes(json.dumps(self.__dict__).encode('utf-8'))

    @staticmethod
    def from_bytes(mess: bytes):
        data = json.loads(mess.decode('utf-8'))
        record = Record(**data)
        return record
