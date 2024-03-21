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

# Configuration de la connexion Hive
hive_conn = hive.Connection(host="127.0.0.1", port=10000)

# Configuration du client HDFS
client = InsecureClient('http://localhost:9870', user='hadoop')

# Chemin de destination dans HDFS
hdfs_destination = "/data/upload/"

# Table de stockage des données
hive_table = "feedback_data_v1"
orc_table = "feedback_data_v2"

# Fonction pour envoyer le fichier JSON vers HDFS
def send_to_hdfs(file_content, file_name):
    try:
        # Écrire le contenu du fichier dans HDFS
        with client.write(os.path.join(hdfs_destination, file_name), encoding='utf-8') as writer:
            writer.write(file_content)
        print("Fichier JSON envoyé avec succès vers Hadoop.")
    except Exception as e:
        print(f"Erreur lors de l'envoi du fichier JSON vers Hadoop : {e}")

# Fonction pour charger les données JSON dans Hive
def load_data_to_hive(file_name):
    try:
        # Exécuter une requête Hive pour charger le fichier JSON dans la table
        hive_conn.cursor().execute(f"LOAD DATA INPATH '{hdfs_destination}' INTO TABLE {hive_table}")
        print(f"Données du fichier JSON '{file_name}' chargées avec succès dans Hive.")
    except Exception as e:
        print(f"Erreur lors du chargement des données JSON dans Hive : {e}")


# Route pour soumettre un feedback
@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    data = request.json

    # Récupérer le nom du fichier joint
    attached_file_name = data.get('attachedfiles', '')

    # Supprimer la clé attachedfilesinput
    key_to_remove = "attachedfilesinput"
    if key_to_remove in data.keys():
        del data[key_to_remove]

    # Générer un identifiant unique
    unique_id = str(uuid.uuid4())

    # Ajouter la date du jour au nom du fichier
    current_date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    file_name = f"feedback_{current_date}_{unique_id}.json"

    # Ajouter l'identifiant unique aux données
    data['unique_id'] = unique_id

    # Envoyer les données JSON vers HDFS
    send_to_hdfs(json.dumps(data), file_name)

    # Charger les données JSON dans Hive
    load_data_to_hive(file_name)

    return jsonify({'message': 'Données envoyées avec succès'})

# Route pour récupérer les feedbacks
@app.route('/api/feedback', methods=['GET'])
def get_feedbacks():
    # Exécuter une requête Hive pour récupérer les feedbacks
    cursor = hive_conn.cursor()
    cursor.execute(f"SELECT * FROM {hive_table}")
    results = cursor.fetchall()

    # Convertir les résultats en JSON
    feedbacks = []
    for row in results:
        feedbacks.append({
            "unique_id": row[0],
            "bootcampname": row[1],
            "prioriteRetour": row[2],
            "typeRetour": row[3],
            "date_feedback": row[4],
            "rating": row[5],
            "comments": row[6],
            "attachedfiles": row[7],
        })

    return jsonify(feedbacks)

# Route pour récupérer un feedback par son identifiant unique
@app.route('/api/feedback/<feedback_id>', methods=['GET'])
def get_feedback_by_id(feedback_id):

    # Exécuter une requête Hive pour récupérer le feedback
    cursor = hive_conn.cursor()
    cursor.execute(f"SELECT * FROM {hive_table} WHERE unique_id = '{feedback_id}'")

    # Vérifier si le feedback existe
    if cursor.rowcount == 0:
        return jsonify({'error': 'Feedback introuvable'}), 404

    # Récupérer le résultat
    row = cursor.fetchone()

    # Convertir le résultat en JSON
    feedback = {
        "unique_id": row[0],
        "bootcampname": row[1],
        "prioriteRetour": row[2],
        "typeRetour": row[3],
        "date_feedback": row[4],
        "rating": row[5],
        "comments": row[6],
        "attachedfiles": row[7],
    }

    return jsonify(feedback)


# Route pour mettre à jour un feedback
@app.route('/api/feedback/<feedback_id>', methods=['PUT'])
def update_feedback(feedback_id):
    data = request.json

    # Exécuter une requête Hive pour mettre à jour le feedback
    cursor = hive_conn.cursor()
    cursor.execute(f"""
        UPDATE {hive_table}
        SET bootcampname = '{data['bootcampname']}',
            prioriteRetour = '{data['prioriteRetour']}',
            typeRetour = '{data['typeRetour']}',
            date_feedback = '{data['date_feedback']}',
            rating = '{data['rating']}',
            comments = '{data['comments']}',
            attachedfiles = '{data['attachedfiles']}'
        WHERE unique_id = '{feedback_id}'
    """)

    # Vérifier si le feedback a été mis à jour
    if cursor.rowcount == 0:
        return jsonify({'error': 'Feedback introuvable'}), 404

    return jsonify({'message': 'Feedback mis à jour avec succès'})

# Route pour supprimer un feedback
@app.route('/api/feedback/<feedback_id>', methods=['DELETE'])
def delete_feedback(feedback_id):

    # Exécuter une requête Hive pour supprimer le feedback
    cursor = hive_conn.cursor()
    cursor.execute(f"DELETE FROM {hive_table} WHERE unique_id = '{feedback_id}'")

    # Vérifier si le feedback a été supprimé
    if cursor.rowcount == 0:
        return jsonify({'error': 'Feedback introuvable'}), 404

    return jsonify({'message': 'Feedback supprimé avec succès'})

if __name__ == '__main__':
    app.run(debug=True)

