import asyncio
from typing import Optional, Coroutine, Callable, Awaitable
import json

import aiormq
import pika

from src.adapters.abc_repository import ApiAbstractRepository
from src.logger.record import Record

from src.config import RABBITMQ_ADDRESS


class RabbitMQRepository(ApiAbstractRepository):
    _connection = None


    async def get_connect(self):
        if self.__class__._connection is not None:
            return self.__class__._connection

        try:
            connection = await aiormq.connect(RABBITMQ_ADDRESS+'//')
        except Exception as e:
            print(f'Error to connect RabbitMQ: {e}')
            connection = None

        self.__class__._connection = connection

        return connection


    async def add(self, record: Record) -> bool:
        connect = await self.get_connect()

        if connect is None:
            return False

        channel = await connect.channel()

        await channel.queue_declare('logger')

        await channel.basic_publish(record.rebytes, routing_key='logger')

        await channel.close()

        return True


    async def aget(self, task: Callable) -> Optional[aiormq.abc.DeliveredMessage]:
        connect = await self.get_connect()

        if connect is None:
            return

        channel = await connect.channel()

        declare = await channel.queue_declare('logger')

        await channel.basic_consume(
            declare.queue,
            task,
            no_ack=True
        )

    def get(self, task: Callable):
        parameters = pika.URLParameters(RABBITMQ_ADDRESS)

        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.basic_consume('logger', task)
        except Exception as e:
            print(f'Ошибка при подключения к RabbitMQ: {e=}')
            return

        try:
            print('Ожидание данных ...')
            channel.start_consuming()
        except Exception as e:
            print(f'Ошибка при получении/ожидании данных от RabbitMQ: {e=}')
            channel.stop_consuming()

        connection.close()

        return


class RabbitMQFakeRepository(ApiAbstractRepository):
    _memory = []

    async def add(self, record: Record):
        self.__class__._memory.append(record.rebytes)
        return True

    async def aget(self, task: Callable):
        declare = FakeDeliveredMessage(self.__class__._memory.pop())

        await task(declare)

    def get(self, task: Callable):
        task(self.__class__._memory.pop())
        return


class FakeDeliveredMessage:
    def __init__(self, mess):
        self.body = mess





# async def exi_worker():
#     b = RabbitMQRepository()
#
#     while True:
#         await b.get(process)
#
#         await asyncio.sleep(5)
#
#
# async def process(record: aiormq.abc.DeliveredMessage):
#     record = json.loads(record.body.decode('utf-8'))
#     print(record)


# async def example(a: RabbitMQRepository):
#     for i in range(5):
#         for j in range(100):
#             print(f'add {i=}, {j=}')
#             record = Record(user='avkritsky', project=f'autoblock{i}',
#                             ref='test_logger', level=i,
#                             mess=f'{i}:{j}: Test message for Integration test')
#
#             await a.add(record)
#
#
# if __name__ == '__main__':
#     a = RabbitMQRepository()
#     asyncio.run(example(a))
