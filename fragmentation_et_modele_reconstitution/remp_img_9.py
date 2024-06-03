import os
import sqlite3

# Se connecter à la base de données
conn = sqlite3.connect('puzzle2.db')
cursor = conn.cursor()
cursor.execute("Delete from Images9Pieces")
cursor.execute('''CREATE TABLE IF NOT EXISTS Images9Pieces (
                    id INTEGER PRIMARY KEY,
                    nom TEXT,
                    image BLOB,
                    image_complete_id INTEGER,
                    FOREIGN KEY (image_complete_id) REFERENCES ImagesCompletes(id)
                )''')

# Chemin du dossier contenant les images
dossier_images = "C:\\Users\\LENOVO\\Desktop\\pp1"

# Boucle à travers les dossiers dans le dossier principal
for subdir, _, files in os.walk(dossier_images):
    if "image_" in subdir:  # Vérifiez si le sous-dossier contient "image_"
        # Extraire l'ID de l'image complète à partir du nom du sous-dossier
        subdir_components = subdir.split("_")
        if len(subdir_components) == 2:  # Vérifiez que le nom du sous-dossier est dans le bon format
            image_complete_id = int(subdir_components[1])

            for filename in files:
                if filename.endswith(".png"):  # Assurez-vous que le fichier est une image
                    # Ouvrir et lire l'image en mode binaire
                    with open(os.path.join(subdir, filename), "rb") as f:
                        image_data = f.read()

                    # Insérer l'image dans la table Images9Pieces
                    cursor.execute("INSERT INTO Images9Pieces (nom, image, image_complete_id) VALUES (?, ?, ?)", (filename, sqlite3.Binary(image_data), image_complete_id))

# Valider les changements
conn.commit()

# Fermer la connexion
conn.close()
