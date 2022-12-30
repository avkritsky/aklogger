import abc

from src.logger.record import Record

class ApiAbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add(self, record: Record):
        pass
