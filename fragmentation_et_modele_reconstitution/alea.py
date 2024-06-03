import cv2
import numpy as np
import os
import random

def fragment_and_shuffle(image_path, fragment_size):
    # Chargement de  l'image
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Erreur: Impossible de charger l'image à partir de {image_path}")
        return None
    
    # Obtenir les dimensions de l'image
    height, width = image.shape[:2]
    
    # Calcul du  nombre de fragments en hauteur et en largeur
    num_frag_height = height // fragment_size
    num_frag_width = width // fragment_size
    
    # Liste pour stocker les fragments
    fragments = []
    
    #  boucle pour découper l'image en fragments
    for i in range(num_frag_height):
        for j in range(num_frag_width):
            fragment = image[i*fragment_size:(i+1)*fragment_size, j*fragment_size:(j+1)*fragment_size]
            fragments.append(fragment)
    
    # Mélange des  fragments dans un ordre aléatoire
    random.shuffle(fragments)
    
    # Création d'une image vide pour reconstituer les fragments
    shuffled_image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Réassemblement des fragments dans l'image complète
    idx = 0
    for i in range(num_frag_height):
        for j in range(num_frag_width):
            shuffled_image[i*fragment_size:(i+1)*fragment_size, j*fragment_size:(j+1)*fragment_size] = fragments[idx]
            idx += 1
    
    return shuffled_image

def process_images_in_directory(input_dir, output_dir, fragment_size):
    if not os.path.exists(input_dir):
        print(f"Erreur: Le dossier d'entrée '{input_dir}' n'existe pas.")
        return
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Parcours de  toutes les images dans le dossier d'entrée
    for filename in os.listdir(input_dir):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".jfif")):
            # Chemin complet de l'image d'entrée
            input_path = os.path.join(input_dir, filename)
            
            shuffled_image = fragment_and_shuffle(input_path, fragment_size)
            
            if shuffled_image is not None:
                # Chemin complet de l'image de sortie
                output_path = os.path.join(output_dir, f"{filename.split('.')[0]}.jpg")
                
                # Enregistrement de  l'image réassemblée dans le dossier de sortie
                cv2.imwrite(output_path, shuffled_image)

# Exemple d'utilisation
input_dir = r"C:\Users\Hp\Desktop\comp"  # Dossier contenant les images d'entrée
output_dir = r"C:\Users\Hp\Desktop\alea"  # Dossier de sortie pour les images réassemblées
fragment_size = 100  # Taille des fragments en pixels

process_images_in_directory(input_dir, output_dir, fragment_size)
