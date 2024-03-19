import subprocess

# Chemin du fichier JSON à envoyer vers HDFS
json_file_path = "feedback.json"

# Chemin de destination dans HDFS
hdfs_destination = "/data/upload/feedback.json"

# Commande hdfs dfs pour copier le fichier JSON vers HDFS
copy_command = f"hdfs dfs -copyFromLocal {json_file_path} {hdfs_destination}"

# Exécution de la commande
try:
    subprocess.run(copy_command, shell=True, check=True)
    print("Fichier JSON envoyé avec succès vers Hadoop.")
except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'envoi du fichier JSON vers Hadoop : {e}")
