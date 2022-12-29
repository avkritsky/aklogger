from urllib import request, parse

from src.adapters.abc_repository import Repository
from src.logger.models import Record
from src.config import API_ROUTE


class ApiRepository(Repository):

    def __init__(self):
        self.api_route = API_ROUTE

    def add(self, record: Record) -> bool:
        try:
            data = parse.urlencode(record.__dict__).encode()
            req = request.Request(self.api_route, data=data, method='POST')
            resp = request.urlopen(req, timeout=3)
            print(resp.read())
        except Exception:
            return False

        return True


class ApiFakeRepository(Repository):

    def __init__(self):
        self.api_route = API_ROUTE
        self.sended = []

    def add(self, record: Record) -> bool:
        self.sended.append(record)
        return True
