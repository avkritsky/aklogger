import pytest

from src.logger.record import Record
from src.adapters.repository_rabbitmq import RabbitMQFakeRepository, FakeDeliveredMessage


@pytest.mark.asyncio
async def test_add_to_repo():
    a = RabbitMQFakeRepository()

    record = Record(user='avkritsky', project='autoblock', ref='test_add_to_repo', level=4,
                    mess='Test message for Unit test RabbitMQ')

    status = await a.add(record)

    assert status is True
    assert record.rebytes in a.__class__._memory


@pytest.mark.asyncio
async def test_load_from_repo():
    b = RabbitMQFakeRepository()

    record = Record(user='avkritsky', project='autoblock', ref='test_load_from_repo', level=4,
                    mess='Test message for Unit test RabbitMQ2')

    await b.add(record)

    async def rprint(mess: FakeDeliveredMessage, arec = record):
        record = Record.from_bytes(mess.body)

        assert arec == record

    await b.aget(rprint)
