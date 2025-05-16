import requests
import pika
import time
import json
import os

API_URL = os.getenv("API_URL", "http://api:5000/generate_vote")  # hostname desde docker-compose
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", 5))

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
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
