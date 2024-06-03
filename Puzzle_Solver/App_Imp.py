import os
import sqlite3
from PIL import Image
import numpy as np
from io import BytesIO
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])

UPLOAD_FOLDER = './upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def cut_puzzle_piece(image_path, rows, cols):
    image = Image.open(image_path)
    width, height = image.size
    piece_width = width // cols
    piece_height = height // rows
    pieces = []

    for i in range(rows):
        for j in range(cols):
            left = j * piece_width
            top = i * piece_height
            right = (j + 1) * piece_width
            bottom = (i + 1) * piece_height
            piece = image.crop((left, top, right, bottom))
            piece_data = BytesIO()
            piece.save(piece_data, format="JPEG")
            pieces.append(piece_data.getvalue())

    return pieces

def clear_upload_folder():
    folder = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    try:
        clear_upload_folder()  

        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        image_file = request.files['image']

        if image_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'image.jpg')
        image_file.save(image_path)

        conn = sqlite3.connect('puzzle.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS img_frag (
                            id INTEGER PRIMARY KEY,
                            ref_img INTEGER,
                            fragment BLOB
                        )''')
        cursor.execute("DELETE FROM img_frag")
        with open(image_path, 'rb') as file:
            blob_data = file.read()
            cursor.execute("INSERT INTO img_frag (ref_img, fragment) VALUES (?, ?)", (1, blob_data))
        
        pieces = cut_puzzle_piece(image_path, 3, 3)
        cursor.execute('''CREATE TABLE IF NOT EXISTS puzzle_pieces (
                            id INTEGER PRIMARY KEY,
                            ref_img INTEGER,
                            piece BLOB
                        )''')
        cursor.execute("DELETE FROM puzzle_pieces")
        for piece in pieces:
            cursor.execute("INSERT INTO puzzle_pieces (ref_img, piece) VALUES (?, ?)", (1, piece))
        
        conn.commit()
        cursor.close()
        conn.close()

        image_url = request.host_url + 'api/upload-image/images/image.jpg'

        return jsonify({'message': 'File uploaded and saved to database successfully', 'imageUrl': image_url}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-image/images/<filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/fragment-image', methods=['GET'])
def get_fragments():
    try:
        conn = sqlite3.connect('puzzle.db')
        cursor = conn.cursor()
        cursor.execute("SELECT piece FROM puzzle_pieces")
        rows = cursor.fetchall()
        pieces = [BytesIO(row[0]).getvalue() for row in rows]
        base_url = request.host_url + 'api/fragment-image/images/'
        piece_urls = [base_url + f'piece_{i}.jpg' for i in range(len(pieces))]

        temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'temp')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        for i, piece in enumerate(pieces):
            with open(os.path.join(temp_dir, f'piece_{i}.jpg'), 'wb') as f:
                f.write(piece)

        cursor.close()
        conn.close()

        return jsonify(piece_urls)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/fragment-image/images/<filename>')
def get_piece(filename):
    temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'temp')
    return send_from_directory(temp_dir, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5005)
