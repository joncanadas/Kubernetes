from flask import Flask, jsonify, render_template
import random
import uuid
from datetime import datetime

app = Flask(__name__, template_folder='templates')

# Lista para guardar los votos
votos_guardados = []

# Datos base
deportistas_generales = [
    "Rafael Nadal", "Fernando Alonso", "Pau Gasol", "Andres Iniesta", "Mireia Belmonte"
]

futbolistas_actual = [
    "Pedri Gonzalez", "Raphinha", "Ousmane Dembele", "Kylian Mbappe", "Lamine Yamal"
]

regiones = ["Andalucía", "Cataluña", "Madrid", "Valencia", "Galicia", "Euskadi"]
razones = ["Es un referente", "Me gusta su estilo", "Siempre lo da todo", "Ha hecho historia"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/votes')
def get_votes():
    return jsonify(votos_guardados)  # Devuelve la lista de votos

@app.route('/generate_vote', methods=['GET'])
def generate_vote():
    topic = random.choice(["mejor_deportista", "mejor_futbolista"])
    if topic == "mejor_deportista":
        atleta = random.choice(deportistas_generales)
    else:
        atleta = random.choice(futbolistas_actual)

    voto = {
        "voter_id": str(uuid.uuid4()),
        "age": random.randint(18, 65),
        "region": random.choice(regiones),
        "topic": topic,
        "athlete": atleta,
        "reason": random.choice(razones),
        "timestamp": datetime.utcnow().isoformat()
    }

    votos_guardados.append(voto)  # Guarda el voto
    return jsonify(voto)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
