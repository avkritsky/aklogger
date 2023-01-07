import json

from aiohttp import web

from src.logger.record import Record
from src.adapters.repository_rabbitmq import RabbitMQRepository


routes = web.RouteTableDef()


@routes.post('/v1/add')
async def add_record_route(request: web.Request):
    try:
        data = await request.read()
    except Exception as e:
        print(f'Ошибка получения данных от клиента: {e}')
        return web.Response(status=400, reason=f'Can\'t read data from request: {e}')
    print(data)

    try:
        data = json.loads(data.decode(encoding='utf-8'))
    except Exception as e:
        return web.Response(status=400, reason=f'Can\'t load data: {e}')

    try:
        record = Record(**data)
        print(record)
    except TypeError:
        return web.Response(status=406, reason=f'Unknown data')

    rabbit = RabbitMQRepository()

    try:
        res = await rabbit.add(record)
    except Exception as e:
        print(f'Ошибка сохранения запроса в RabbitMQ: {e}')
        res = None

    if res:
        return web.Response(status=200, text=f'{record.user}:{record.project}:Success')
    else:
        return web.Response(status=400, reason=f'Can\'t upload data to rabbitmq queue')


@routes.get('/v1')
async def get_main_route(request):
    return web.Response(status=200, text='Success')


def init(argv):
    print('Старт сервера API-LOGGER')
    app = web.Application()
    app.add_routes(routes)

    return app


if __name__ == '__main__':
    init([])
