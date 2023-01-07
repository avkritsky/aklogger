import json

import pytest

from src.entrypoints import api_app
from src.logger.record import Record
from src.adapters.repository_rabbitmq import RabbitMQFakeRepository

@pytest.fixture
def cli(event_loop, aiohttp_client):
    app = api_app.init(RabbitMQFakeRepository)

    return event_loop.run_until_complete(aiohttp_client(app))


@pytest.mark.asyncio
async def test_add_record(cli):
    record = Record(user='avkritsky', project='autoblock', ref='test_can_created_exist_logger_by_ref', level=4,
                    mess='Test message for Integration test')
    resp = await cli.post('/v1/add', data=bytes(json.dumps(record.__dict__).encode('utf-8')))

    assert resp.status == 200
    assert await resp.text() == f'{record.user}:{record.project}:Success'


@pytest.mark.asyncio
async def test_bad_data_sending(cli):
    record = {'Test': None}

    resp = await cli.post('/v1/add', data=bytes(json.dumps(record).encode('utf-8')))

    assert resp.status == 406
    assert resp.reason == 'Unknown data. Can not create Record.'

