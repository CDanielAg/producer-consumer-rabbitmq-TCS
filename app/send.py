import argparse

import pika

from config import connection_parameters, declare_hello_queue


def main(message: str) -> None:
    connection = pika.BlockingConnection(connection_parameters())
    channel = connection.channel()
    declare_hello_queue(channel)
    channel.basic_publish(
        exchange="",
        routing_key="hello",
        body=message.encode("utf-8"),
        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
    )
    print(f"[productor] Mensaje enviado: {message}", flush=True)
    connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Envía un mensaje a RabbitMQ")
    parser.add_argument("message", nargs="?", default="¡Hola, RabbitMQ!")
    args = parser.parse_args()
    main(args.message)
