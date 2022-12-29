import abc

from src.logger.models import Record

class Repository(abc.ABC):

    @abc.abstractmethod
    def add(self, record: Record):
        pass
