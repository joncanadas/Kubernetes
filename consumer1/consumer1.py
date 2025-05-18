import pika
import json
import os
from pymongo import MongoClient

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "myuser")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS", "mypass")

MONGO_HOST = os.getenv("MONGO_HOST", "mongodb")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
db = mongo_client.encuestas
collection = db.votos

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='encuestas', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='encuestas', queue=queue_name, routing_key="encuesta.*")

def callback(ch, method, properties, body):
    vote = json.loads(body)
    collection.insert_one(vote)
    print(f"[✓] Voto almacenado en MongoDB: {vote['athlete']} ({vote['topic']})")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("[*] Esperando mensajes. Para salir presiona CTRL+C")
channel.start_consuming()
