from config import settings
from broker.listener import callback
from broker.rabbitmq_client import RabbitRPCClient
import os

print(os.getcwd())
if __name__ == '__main__':
    rpc = RabbitRPCClient(
        receiving_queue="coupon",
        callback=callback,
        exchange_name="headers_exchange",
        headers={
            settings.APP_NAME: True
        },
        headers_match_all=True
    )
    rpc.connect()
    rpc.consume()

