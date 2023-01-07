import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from datetime import datetime
from multiprocessing import current_process, Queue, Process

from src.logger.record import Record
from src.adapters.repository_rabbitmq import RabbitMQRepository
from src.config import WORKERS_COUNT


def worker(queue: Queue):
    print(f'start worker {current_process().name}')
    while True:
        try:
            body = queue.get(block=True)
            print(f'{current_process().name}: получил тело: {body}')
            write_record(body)
        except Exception as e:
            print(f'Ошибка исполнения работника: {e=}')
            break
    print(f'end worker {current_process().name}')


def write_record(body):
    try:
        # получаем запись
        record = Record.from_bytes(body)

        print(os.path.exists(f'/var/log/{record.user}/{record.project}'))
        if not os.path.exists(f'/var/log/{record.user}/{record.project}'):
            print(f'{current_process().name}: Создаю папку -> /var/log/{record.user}/{record.project}')
            os.mkdir(f'/var/log/{record.user}/{record.project}')

        # записываем лог
        with open(f'/var/log/{record.user}/{record.project}/{record.ref}.txt', 'a') as file:
            file.write(f'{datetime.now()} - l{record.level}: {record.mess}\n')
    except Exception as e:
        print(e)


def start_workers():
    queue = Queue(0)

    def add_to_queue(*args, queue: Queue = queue):
        channel, method_frame, _, body = args
        print(f'Добавляю в очередь тело: {body}')
        queue.put(body)
        # подтверждаем получение
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    print('Запуск воркеров')
    for i in range(WORKERS_COUNT):
        process = Process(target=worker, args=(queue,))
        process.start()

    print('Запуск потребителя RabbitMQ')
    repo = RabbitMQRepository()
    while True:
        try:
            repo.get(add_to_queue)
        except Exception as e:
            print(f'Ошибка исполнения работника: {e=}')
            break


if __name__ == '__main__':
    start_workers()