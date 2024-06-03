import os
import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, UpSampling2D, Input, Cropping2D, Dropout, BatchNormalization
from tensorflow.keras.regularizers import l2
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array, load_img, ImageDataGenerator
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
from tensorflow.keras.callbacks import ReduceLROnPlateau, LearningRateScheduler
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

# Load image function
def load_image(file_path, target_size=None):
    img = load_img(file_path, target_size=target_size)
    return img_to_array(img) / 255.0

# Directories for scrambled and original images
scrambled_image_dir = '/kaggle/input/aleatoire/alea'
original_image_dir = '/kaggle/input/ahlam5/comp'

# Define a consistent target size
target_size = (256, 256)

# Load and process images
X = []
y = []

# Get list of files in each directory
scrambled_image_files = sorted(os.listdir(scrambled_image_dir))
original_image_files = sorted(os.listdir(original_image_dir))

# Ensure the same number of files in both directories
assert len(scrambled_image_files) == len(original_image_files), "Mismatched number of images."

for scrambled_image_file, original_image_file in zip(scrambled_image_files, original_image_files):
    scrambled_image_path = os.path.join(scrambled_image_dir, scrambled_image_file)
    original_image_path = os.path.join(original_image_dir, original_image_file)
    
    scrambled_image = load_image(scrambled_image_path, target_size=target_size)
    original_image = load_image(original_image_path, target_size=target_size)
    
    # Ensure both images have the same shape
    assert scrambled_image.shape == original_image.shape, "Images must be the same shape."
    
    # Append to dataset
    X.append(scrambled_image)
    y.append(original_image)

# Convert lists to numpy arrays
X = np.array(X)
y = np.array(y)

# Split the data into training (80%) and validation (20%) sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Data augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True
)

# Define the autoencoder model
def build_model(input_shape):
    input_img = Input(shape=input_shape)
    
    x = Conv2D(64, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-4))(input_img)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Dropout(0.3)(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-4))(x)
    x = BatchNormalization()(x)
    x = MaxPooling2D((2, 2), padding='same')(x)
    x = Dropout(0.3)(x)
    x = Conv2D(256, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-4))(x)
    x = BatchNormalization()(x)
    encoded = MaxPooling2D((2, 2), padding='same')(x)
    
    x = Conv2D(256, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-4))(encoded)
    x = BatchNormalization()(x)
    x = UpSampling2D((2, 2))(x)
    x = Dropout(0.3)(x)
    x = Conv2D(128, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-4))(x)
    x = BatchNormalization()(x)
    x = UpSampling2D((2, 2))(x)
    x = Dropout(0.3)(x)
    x = Conv2D(64, (3, 3), activation='relu', padding='same', kernel_regularizer=l2(1e-4))(x)
    x = BatchNormalization()(x)
    x = UpSampling2D((2, 2))(x)
    x = Dropout(0.3)(x)
    x = Conv2D(3, (3, 3), activation='sigmoid', padding='same')(x)
    
    # Ensure output size matches input size
    height_crop = (x.shape[1] - input_img.shape[1]) // 2
    width_crop = (x.shape[2] - input_img.shape[2]) // 2
    if height_crop > 0 or width_crop > 0:
        x = Cropping2D(((height_crop, height_crop), (width_crop, width_crop)))(x)

    autoencoder = Model(input_img, x)
    return autoencoder

# Set initial learning rate
initial_lr = 2.5e-4

# Build and compile the model
model = build_model(X.shape[1:])
optimizer = Adam(learning_rate=initial_lr)
model.compile(optimizer=optimizer, loss='mean_squared_error')

# Learning rate scheduler
def scheduler(epoch, lr):
    if epoch % 50 == 0 and epoch != 0:
        lr = lr * 0.5
    return lr

# Callbacks for learning rate reduction
callbacks = [
    ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, min_lr=0.00001),
    LearningRateScheduler(scheduler)
]

# Train the model
history = model.fit(datagen.flow(X_train, y_train, batch_size=1), epochs=100, shuffle=True, validation_data=(X_val, y_val), callbacks=callbacks)

# Extract training history
train_loss = history.history['loss']
val_loss = history.history['val_loss']

# Convert losses to percentage
train_loss_percent = [loss * 100 for loss in train_loss]
val_loss_percent = [loss * 100 for loss in val_loss]

# Plot training history
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(train_loss_percent, label='Training Loss')
plt.plot(val_loss_percent, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss (%)')
plt.legend()

# Evaluate the model on the test set
test_loss = model.evaluate(X_val, y_val, batch_size=1)
print("Test Loss:", test_loss * 100, "%")

# Use KNN for evaluation on the test set
# Flatten images for KNN
X_flat = X_val.reshape(X_val.shape[0], -1)
y_flat = y_val.reshape(y_val.shape[0], -1)

# Determine n_neighbors based on the size of the validation set
n_neighbors = min(3, len(X_val))

# Train KNN
knn = KNeighborsRegressor(n_neighbors=n_neighbors)
knn.fit(X_flat, y_flat)

# Predict with KNN
y_pred_flat = knn.predict(X_flat)
y_pred = y_pred_flat.reshape(y_val.shape)

# Calculate KNN test loss (mean squared error)
knn_test_loss = np.mean((y_val - y_pred) ** 2)
print("KNN Test Loss:", knn_test_loss * 100, "%")

# Display the images
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.title('Scrambled Image')
plt.imshow(X_val[0])

plt.subplot(1, 3, 2)
plt.title('Reconstructed Image (KNN)')
plt.imshow(y_pred[0])

plt.show()

# Save the model
model.save('/kaggle/working/autoencoder_model.h5')
