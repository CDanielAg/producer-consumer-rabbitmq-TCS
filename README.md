# Producer Consumer con RabbitMQ

Recreación del tutorial Hello World de RabbitMQ en Python. El productor envía un
mensaje a la cola 'hello' y el consumidor lo recibe.

## Requisitos

- Docker Desktop o Docker Engine con Compose.
- Python 3.10 o posterior.

## Preparación

~~~bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
docker compose up -d
~~~

RabbitMQ usa el puerto AMQP 5672. La interfaz de administración queda disponible
en 'http://localhost:15672' con usuario y contraseña 'guest'.

## Ejecución manual

En una terminal inicia el consumidor:

~~~bash
.venv\Scripts\python app\receive.py
~~~

En otra terminal ejecuta el productor:

~~~bash
.venv\Scripts\python app\send.py "Hola desde RabbitMQ"
~~~

## Demostración automática

Con RabbitMQ activo:

~~~bash
.venv\Scripts\python scripts\demo.py
~~~

El consumidor se detiene después del primer mensaje y se genera evidencia en
'../docs/evidencia-ejecucion.txt'.

Para detener el servicio:

~~~bash
docker compose down
~~~
