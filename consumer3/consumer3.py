import pika
import json
import os
import time

# Configuración de RabbitMQ
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_USER = os.environ.get("RABBITMQ_USER", "myuser")
RABBITMQ_PASS = os.environ.get("RABBITMQ_PASS", "mypass")

credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)

# Conexión con reintentos
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

futbolistas_actual = [
    "Pedri Gonzalez", "Raphinha", "Ousmane Dembele", "Kylian Mbappe", "Lamine Yamal"
]

def detectar_alerta(voto):
    edad = voto['age']
    atleta = voto['athlete']
    region = voto['region']

    if edad > 60 and atleta in futbolistas_actual:
        return f"Alerta: Persona mayor votó a un futbolista actual ({atleta})"
    if region in ["Galicia", "Euskadi"] and atleta in ["Kylian Mbappe", "Ousmane Dembele"]:
        return f"Alerta: Ciudadano de {region} votó por {atleta}, extranjero"
    if edad < 20 and atleta == "Lamine Yamal":
        return f"Alerta: Jóvenes apoyan a Lamine Yamal"

    return None

def callback(ch, method, properties, body):
    voto = json.loads(body)
    alerta = detectar_alerta(voto)
    if alerta:
        print(alerta)
        print(f"   Datos: {voto}")
    else:
        print("Voto recibido sin alerta especial.")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Consumer3 escuchando alertas sociológicas...")
channel.start_consuming()
