from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import base64

app = Flask(__name__)
CORS(app)

# Route pour récupérer les données de la table ImagesCompletes
@app.route('/api/ImagesCompletes', methods=['GET'])
def get_images_completes():
    try:
        conn = sqlite3.connect('puzzle2.db')
        cursor = conn.cursor()
        cursor.execute('SELECT image FROM ImagesCompletes')
        rows = cursor.fetchall()
        image_urls = []
        for row in rows:
            base64_image = base64.b64encode(row[0]).decode('utf-8')
            image_urls.append(f"data:image/png;base64,{base64_image}")
        conn.close()
        return jsonify(image_urls), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)
