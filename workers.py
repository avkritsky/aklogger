import os.path

from datetime import datetime
from multiprocessing import Pool, current_process

from src.logger.record import Record
from src.adapters.repository_rabbitmq import RabbitMQRepository
from src.config import WORKERS_COUNT


def worker():
    print(f'start worker {current_process().name}')
    repo = RabbitMQRepository()
    try:
        repo.get(write_record)
    except Exception as e:
        print(f'Ошибка исполнения работника: {e=}')
    print(f'end worker {current_process().name}')


def write_record(channel, method_frame, _, body):
    try:
        # получаем запись
        record = Record.from_bytes(body)

        # подтверждаем получение
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)

        if not os.path.exists(f'/var/log/{record.user}/{record.project}'):
            os.mkdir(f'/var/log/{record.user}/{record.project}')

        # записываем лог
        with open(f'/var/log/{record.user}/{record.project}/{record.ref}.txt', 'a') as file:
            file.write(f'{datetime.now()} - l{record.level}: {record.mess}\n')
    except Exception as e:
        print(e)




def start_workers():
    with Pool(WORKERS_COUNT) as pool:
        for _ in range(WORKERS_COUNT):
            pool.apply_async(worker)

        pool.close()
        pool.join()



if __name__ == '__main__':
    start_workers()