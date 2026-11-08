import os

import pika


def connection_parameters() -> pika.ConnectionParameters:
    credentials = pika.PlainCredentials(
        os.getenv("RABBITMQ_USER", "guest"),
        os.getenv("RABBITMQ_PASSWORD", "guest"),
    )
    return pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", "5672")),
        credentials=credentials,
        heartbeat=30,
        blocked_connection_timeout=30,
    )


def declare_hello_queue(channel: pika.adapters.blocking_connection.BlockingChannel) -> None:
    channel.queue_declare(
        queue="hello",
        durable=True,
        arguments={"x-queue-type": "quorum"},
    )
