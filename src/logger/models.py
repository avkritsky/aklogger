from typing import Optional

from src.logger.record import Record, Level
from src.adapters.abc_repository import ApiAbstractRepository
from src.adapters.repository_api import ApiRepository


class Logger:
    _instance: dict = {}

    def __init__(self,
                 ref: str,  # уникальный параметр, будет использован в имени лога (номер/имя таска, имя проекта и т.д.)
                 user: str = 'none',
                 project: str = 'common',
                 level: int = 4,
                 api_repository: ApiAbstractRepository = ApiRepository()):
        if ref in self.__class__._instance:
            self.__dict__ = self.__class__._instance[ref].__dict__
        else:
            self.user = user
            self.project = project
            self.ref = ref
            self.last_log: Optional[Record] = None
            self.level = level
            self.repository = api_repository
            self.__class__._instance[ref] = self

    def debug(self, mess: str) -> bool:
        if self.level < Level.DEBUG.value:
            return False
        self._create_record(mess, Level.DEBUG.value)
        return True

    def warning(self, mess: str) -> bool:
        if self.level < Level.WARNING.value:
            return False
        self._create_record(mess, Level.WARNING.value)
        return True

    def info(self, mess: str) -> bool:
        if self.level < Level.INFO.value:
            return False
        self._create_record(mess, Level.INFO.value)
        return True

    def critical(self, mess: str) -> bool:
        if self.level < Level.CRITICAL.value:
            return False
        self._create_record(mess, Level.CRITICAL.value)
        return True

    def error(self, mess: str) -> bool:
        if self.level < Level.ERROR.value:
            return False
        self._create_record(mess, Level.ERROR.value)
        return True

    def _create_record(self, mess: str, level: int):
        if not isinstance(mess, str):
            raise NotValidMessage('Your message not STR!')

        new_record = Record(user=self.user,
                            project=self.project,
                            ref=self.ref,
                            level=level,
                            mess=mess)
        self.last_log = new_record
        self._save_log()


    def _save_log(self):
        """Метод отправляет лог в API"""
        self.repository.add(self.last_log)


class NotValidMessage(Exception):
    pass
