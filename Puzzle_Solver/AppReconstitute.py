import os
import io
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np
import base64

app = Flask(__name__)
CORS(app)

# Load your model
model = tf.keras.models.load_model('C:\\Users\\LENOVO\\Desktop\\ReconstitutionPuzzle\\Model_reconstitution\\image_reconstruction_model_1.h5')

UPLOAD_FOLDER = 'upload'
IMAGE_FILE = 'image.jpg' 

def preprocess_image(image_path):
    image = Image.open(image_path)
    image = image.resize((256, 256))
    image_array = np.array(image) / 255.0 
    return image_array

def reconstruct_image(image_array):
    reconstructed_image = model.predict(np.expand_dims(image_array, axis=0))
    return reconstructed_image

@app.route('/api/reconstruct-image', methods=['POST'])
def reconstruct_image_route():
    try:
        image_path = os.path.join(UPLOAD_FOLDER, IMAGE_FILE)
        image_array = preprocess_image(image_path)
        reconstructed_image = reconstruct_image(image_array)
        
        # Rescale the reconstructed image back to [0, 255]
        reconstructed_image = (reconstructed_image[0] * 255).astype('uint8')
        
        reconstructed_image_pil = Image.fromarray(reconstructed_image, 'RGB')
        buffered = io.BytesIO()
        reconstructed_image_pil.save(buffered, format="PNG")
        reconstructed_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        reconstructed_url = f"data:image/png;base64,{reconstructed_base64}"

        return jsonify({'reconstructedImage': reconstructed_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5007)
