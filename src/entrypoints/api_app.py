import json

from aiohttp import web

from src.logger.record import Record
from src.adapters.repository_rabbitmq import RabbitMQRepository

routes = web.RouteTableDef()

@routes.post('/v1/add')
async def add_record_route(request: web.Request):
    data = await request.read()

    try:
        data = json.loads(data.decode(encoding='utf-8'))
    except Exception as e:
        return web.Response(status=400, text=f'Can\'t read data: {e}')

    try:
        record = Record(**data)
    except TypeError:
        return web.Response(status=406, text=f'Unknown data')

    rabbit = RabbitMQRepository()
    # print(f'Пользователь {record.user} прислал сообщение: {record.mess}')
    res = await rabbit.add(record)

    if res:
        return web.Response(status=200, text=f'{record.user}:{record.project}:Success')
    else:
        return web.Response(status=400, text=f'Can\'t upload data to rabbitmq queue')

@routes.get('/v1')
async def get_main_route(request):
    return web.Response(status=200, text='Success')


def init(argv):
    app = web.Application()
    app.add_routes(routes)

    return app
