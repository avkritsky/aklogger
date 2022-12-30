from urllib import request, parse
import json

from src.adapters.abc_repository import ApiAbstractRepository
from src.logger.record import Record
from src.config import API_ADD_RECORD


class ApiRepository(ApiAbstractRepository):

    def __init__(self):
        self.api_route = API_ADD_RECORD

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


class ApiFakeRepository(ApiAbstractRepository):

    def __init__(self):
        self.api_route = API_ADD_RECORD
        self.sended = []

    def add(self, record: Record) -> bool:
        self.sended.append(record)
        return True
