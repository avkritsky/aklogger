import abc
import json
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from urllib import request


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


class ApiAbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, record: Record):
        pass


class ApiRepository(ApiAbstractRepository):

    def __init__(self, api_route: str = 'http://0.0.0.0:7007/v1/add'):
        self.api_route = api_route

    def add(self, record: Record) -> bool:
        try:
            req = request.Request(self.api_route,
                                  data=bytes(json.dumps(record.__dict__), encoding='utf-8'),
                                  method='POST')
            resp = request.urlopen(req, timeout=3)
            print(resp.read())
        except Exception as e:
            print(f'{e=}')
            return False

        return True


class Logger:
    _instance: dict = {}

    def __init__(self,
                 ref: str,  # уникальный параметр, будет использован в имени лога (номер/имя таска, имя проекта и т.д.)
                 user: str = 'none',
                 project: str = 'common',
                 level: int = 4,
                 api_route: str = 'http://0.0.0.0:7007/v1/add',
                 api_repository: ApiAbstractRepository = None):
        if ref in self.__class__._instance:
            self.__dict__ = self.__class__._instance[ref].__dict__
        else:
            self.user = user
            self.project = project
            self.ref = ref
            self.last_log: Optional[Record] = None
            self.level = level
            if api_repository is None:
                self.repository = ApiRepository(api_route)
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


if __name__ == '__main__':
    logger = Logger(ref='test_logger', user='avkritsky', project='logger', level=4)

    logger.info('Стартовое сообщение')
    logger.debug('Дебаг инфа')
    logger.critical('Критикал инфа, ух ты')