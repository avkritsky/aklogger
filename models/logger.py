from dataclasses import dataclass
from typing import Optional

from models import record


class Logger:
    _instance: dict = {}

    def __init__(self, ref: str, user: str = 'none', project: str = 'common', level: int = 4):
        if ref in self.__class__._instance:
            self.__dict__ = self.__class__._instance[ref].__dict__
        else:
            self.user = user
            self.project = project
            self.ref = ref
            self.last_log: Optional[record.Record] = None
            self.level = level
            self.__class__._instance[ref] = self

    def debug(self, mess: str) -> bool:
        if self.level < record.Level.DEBUG.value:
            return False
        self._create_record(mess, record.Level.DEBUG.value)
        return True

    def warning(self, mess: str) -> bool:
        if self.level < record.Level.WARNING.value:
            return False
        self._create_record(mess, record.Level.WARNING.value)
        return True

    def info(self, mess: str) -> bool:
        if self.level < record.Level.INFO.value:
            return False
        self._create_record(mess, record.Level.INFO.value)
        return True

    def critical(self, mess: str) -> bool:
        if self.level < record.Level.CRITICAL.value:
            return False
        self._create_record(mess, record.Level.CRITICAL.value)
        return True

    def error(self, mess: str) -> bool:
        if self.level < record.Level.ERROR.value:
            return False
        self._create_record(mess, record.Level.ERROR.value)
        return True

    def _create_record(self, mess: str, level: int):
        if not isinstance(mess, str):
            raise NotValidMessage('Your message not STR!')

        new_record = record.Record(user=self.user,
                                   project=self.project,
                                   ref=self.ref,
                                   level=level,
                                   mess=mess)
        self.last_log = new_record
        self._save_log()


    def _save_log(self):
        """Метод отправляет лог в API"""
        ...


class NotValidMessage(Exception):
    pass
