import os

API_LOGGER = 'http://0.0.0.0:7007'
API_ADD_RECORD = f'{API_LOGGER}/v1/add'

# RABBITMQ_ADDRESS = f"amqp://kav:{os.getenv('RABBIT_PASSWORD')}@localhost:5672//"
RABBITMQ_ADDRESS = f"amqp://kav:???@localhost:5672"