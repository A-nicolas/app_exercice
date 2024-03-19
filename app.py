from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import uuid
from datetime import datetime
from hdfs import InsecureClient
from pyhive import hive

app = Flask(__name__)
CORS(app)

# Configuration du client HDFS
client = InsecureClient('http://localhost:9870', user='hadoop')

# Chemin de destination dans HDFS
hdfs_destination = "/data/upload/"

# Fonction pour envoyer le fichier JSON vers HDFS
def send_to_hdfs(file_content, file_name):
    try:
        # Écrire le contenu du fichier dans HDFS
        with client.write(os.path.join(hdfs_destination, file_name), encoding='utf-8') as writer:
            writer.write(file_content)
        print("Fichier JSON envoyé avec succès vers Hadoop.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du fichier JSON vers Hadoop : {e}")


# Route pour recevoir les données JSON du formulaire et les envoyer vers HDFS
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.json

    # Récupérer le nom du fichier joint
    attached_file_name = data.get('attachedfiles', '')

    # Générer un identifiant unique
    unique_id = str(uuid.uuid4())

    # Ajouter la date du jour au nom du fichier
    current_date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    file_name = f"feedback_{current_date}_{unique_id}.json"

    # Ajouter l'identifiant unique aux données
    data['unique_id'] = unique_id
    
    # Envoyer les données JSON directement vers HDFS
    send_to_hdfs(json.dumps(data), file_name)

    return jsonify({'message': 'Données envoyées avec succès'})

if __name__ == '__main__':
    app.run(debug=True)
