import argparse

import pika

from config import connection_parameters, declare_hello_queue


def main(once: bool = False) -> None:
    connection = pika.BlockingConnection(connection_parameters())
    channel = connection.channel()
    declare_hello_queue(channel)

    def callback(
        current_channel: pika.adapters.blocking_connection.BlockingChannel,
        method: pika.spec.Basic.Deliver,
        _properties: pika.spec.BasicProperties,
        body: bytes,
    ) -> None:
        message = body.decode("utf-8")
        print(f"[consumidor] Mensaje recibido: {message}", flush=True)
        current_channel.basic_ack(delivery_tag=method.delivery_tag)
        if once:
            current_channel.stop_consuming()

    channel.basic_consume(queue="hello", on_message_callback=callback)
    print("[consumidor] Esperando mensajes. Presiona Ctrl+C para salir.", flush=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consume mensajes desde RabbitMQ")
    parser.add_argument(
        "--once",
        action="store_true",
        help="Finaliza después de recibir un mensaje",
    )
    args = parser.parse_args()
    main(once=args.once)
