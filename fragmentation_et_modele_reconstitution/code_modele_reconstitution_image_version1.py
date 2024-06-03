import os
import numpy as np
import cv2
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D, Input, Cropping2D, ZeroPadding2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import matplotlib.pyplot as plt

# Chargement des images 
def load_image(file_path, target_size=None):
    img = load_img(file_path, target_size=target_size)
    return img_to_array(img) / 255.0

# Définir les chemins des répertoires
scrambled_image_dir = '/kaggle/input/fragment/alea'
original_image_dir = '/kaggle/input/base-de/comp'

# Définir une taille cible cohérente (par exemple, 256x256)
target_size = (256, 256)

# Chargement et traitement des images
X = []
y = []

# Chargement des chemins des images
scrambled_image_paths = sorted([os.path.join(scrambled_image_dir, fname) for fname in os.listdir(scrambled_image_dir)])
original_image_paths = sorted([os.path.join(original_image_dir, fname) for fname in os.listdir(original_image_dir)])

# Vérifier que les deux répertoires contiennent le même nombre d'images
assert len(scrambled_image_paths) == len(original_image_paths), "Les répertoires doivent contenir le même nombre d'images."

# Chargement des images et leur ajout aux datasets X et y
for scrambled_image_path, original_image_path in zip(scrambled_image_paths, original_image_paths):
    scrambled_image = load_image(scrambled_image_path, target_size=target_size)
    original_image = load_image(original_image_path, target_size=target_size)
    
    # Vérification si les deux images ont la même forme
    assert scrambled_image.shape == original_image.shape, "Les images doivent avoir la même forme."
    
    
    X.append(scrambled_image)
    y.append(original_image)

# Convertion des  listes en tableaux numpy
X = np.array(X)
y = np.array(y)

# Définition du modèle
def build_model(input_shape):
    input_img = Input(shape=input_shape)
    
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(input_img)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same')(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)
    
    x = Conv2D(256, (3, 3), activation='relu', padding='same')(encoded)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)
# Redimensionement des  images    
    height_crop = (x.shape[1] - input_img.shape[1]) // 2
    width_crop = (x.shape[2] - input_img.shape[2]) // 2
    if height_crop > 0 or width_crop > 0:
        x = Cropping2D(((height_crop, height_crop), (width_crop, width_crop)))(x)

    autoencoder = Model(input_img, x)
    return autoencoder

# Construction et compilation du modèle
model = build_model(X.shape[1:])
model.compile(optimizer='adam', loss='binary_crossentropy')

# Entraînement  du modèle avec une régularisation par dropout
history = model.fit(X, y, epochs=100, batch_size=1, shuffle=True, validation_data=(X, y))

# Extraction de l'historique de l'entraînement
train_loss = history.history['loss']
val_loss = history.history['val_loss']

# Convertion des pertes en pourcentage
total_samples = X.shape[0]
train_loss_percent = [loss * 100 for loss in train_loss]
val_loss_percent = [loss * 100 for loss in val_loss]

# Representation de  l'historique de l'entraînement
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(train_loss_percent, label='Training Loss')
plt.plot(val_loss_percent, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss (%)')
plt.legend()

# Évaluer le modèle sur l'ensemble de test
test_loss = model.evaluate(X, y, batch_size=1)

# Afficher la perte de test
print("Test Loss:", test_loss * 100, "%")

# Afficher les images
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.title('Scrambled Image')
plt.imshow(X[0])

plt.subplot(1, 3, 2)
plt.title('Reconstructed Image')
reconstructed_image = model.predict(np.expand_dims(X[0], axis=0))
plt.imshow(reconstructed_image[0])

plt.show()
