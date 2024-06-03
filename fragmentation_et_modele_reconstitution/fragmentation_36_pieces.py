import cv2
import numpy as np
import os

def cut_puzzle_piece(image, rows, cols):
    height, width = image.shape[:2]
    piece_height = height // rows
    piece_width = width // cols
    pieces = []

    for i in range(rows):
        for j in range(cols):
            piece = image[i*piece_height:(i+1)*piece_height, j*piece_width:(j+1)*piece_width]
            pieces.append(piece)

    return pieces

def save_puzzle_pieces(image, rows, cols, output_dir):
    pieces = cut_puzzle_piece(image, rows, cols)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Enregistrement de  l'image fragmentée
    cv2.imwrite(os.path.join(output_dir, "fragmented_image.png"), image)

    # Enregistrement les fragments
    pieces_dir = os.path.join(output_dir, "pieces")
    if not os.path.exists(pieces_dir):
        os.makedirs(pieces_dir)

    for i, piece in enumerate(pieces, start=1):  
        cv2.imwrite(os.path.join(pieces_dir, f"piece_{i}.png"), piece)

# Chemin vers le répertoire contenant les images
database_path = "C:\\Users\\Hp\\Desktop\\test"

# Chemin vers le répertoire pour enregistrer les images fragmentées
output_dir = "C:\\Users\\Hp\\Desktop\\fragmented_images"

# Nombre de lignes et de colonnes dans le puzzle
rows = 6
cols = 6

# Parcours des fichiers dans la base de données
for filename in os.listdir(database_path):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        image_path = os.path.join(database_path, filename)
        image = cv2.imread(image_path)
        
        if image is not None:
            # Création d'un sous-répertoire pour chaque image
            image_output_dir = os.path.join(output_dir, os.path.splitext(filename)[0])
            save_puzzle_pieces(image, rows, cols, image_output_dir)
        else:
            print(f"Impossible de charger l'image : {image_path}")

print("Toutes les images ont été fragmentées et enregistrées dans le dossier spécifié.")
