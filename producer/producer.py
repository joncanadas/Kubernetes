import requests
import pika
import time
import json
import os

# Configuración de RabbitMQ
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
    except pika.exceptions.AMQPConnectionError:
        print(f"RabbitMQ no disponible, reintentando ({i+1}/10)...")
        time.sleep(5)
else:
    print("No se pudo conectar a RabbitMQ tras varios intentos.")
    exit(1)

API_URL = os.getenv("API_URL", "http://api:5000/generate_vote")
INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", 5))

connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=RABBITMQ_HOST,
    credentials=credentials
))
channel = connection.channel()

channel.exchange_declare(exchange='encuestas', exchange_type='topic')

def publish_vote():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            vote = response.json()
            topic = vote['topic']
            routing_key = f"encuesta.{topic}"
            channel.basic_publish(
                exchange='encuestas',
                routing_key=routing_key,
                body=json.dumps(vote)
            )
            print(f"Publicado voto: {routing_key} -> {vote['athlete']}")
    except Exception as e:
        print(f"Error al publicar: {e}")

while True:
    publish_vote()
    time.sleep(INTERVAL_SECONDS)
