import os
import sqlite3

# Se connecter à la base de données
conn = sqlite3.connect('puzzle2.db')
cursor = conn.cursor()

# Chemin du dossier contenant les images
dossier_images = "C:\\Users\\HP\\Desktop\\img_puzzle\\pieces64\\imge20"

# Boucle à travers les fichiers dans le dossier
for filename in os.listdir(dossier_images):
    if filename.endswith(".png"):  # Assurez-vous que le fichier est une image
        # Ouvrir et lire l'image en mode binaire
        with open(os.path.join(dossier_images, filename), "rb") as f:
            image_data = f.read()
        
        # Insérer l'image dans la table ImagesCompletes
        cursor.execute("INSERT INTO Images16Pieces (nom, image, image_complete_id) VALUES (?, ?, 19)", (filename, sqlite3.Binary(image_data)))

# Valider les changements
conn.commit()

# Fermer la connexion
conn.close()
