import pika
import json
import os
import time
from datetime import datetime

RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "myuser")
RABBITMQ_PASS = os.environ.get("RABBITMQ_PASS", "mypass")

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

for i in range(10):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=credentials
        ))
        channel = connection.channel()
        break
    except:
        print(f"[{i+1}/10] Esperando RabbitMQ...")
        time.sleep(5)
else:
    print("No se pudo conectar a RabbitMQ")
    exit(1)

channel.exchange_declare(exchange='encuestas', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='encuestas', queue=queue_name, routing_key='encuesta.#')

def es_alerta(voto):
    if voto['age'] < 25 and voto['athlete'] == "Fernando Alonso":
        return "Alerta: Votante joven eligió a Fernando Alonso"
    if voto['athlete'] == "Kylian Mbappe" and voto['region'] == "Cataluña":
        return "Alerta: Mbappé votado desde Cataluña"
    return None

def callback(ch, method, properties, body):
    voto = json.loads(body)
    alerta = es_alerta(voto)
    if alerta:
        print(f"{alerta}")
        print(f"Datos: {voto}")
    else:
        print("Voto recibido sin alerta.")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Consumer2 esperando votos para alertas...")
channel.start_consuming()
