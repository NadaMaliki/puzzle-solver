from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import base64

app = Flask(__name__)
CORS(app)

@app.route('/api/relatedData36/<int:image_id>', methods=['GET'])
def get_related_data(image_id):
    try:
        conn = sqlite3.connect('puzzle2.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT Pieces.image
            FROM Images32Pieces AS Pieces
            WHERE Pieces.image_complete_id = ?
        ''', (image_id,))
        rows = cursor.fetchall()
        piece_urls = []
        for row in rows:
            base64_piece = base64.b64encode(row[0]).decode('utf-8')
            piece_urls.append(f"data:image/png;base64,{base64_piece}")
        conn.close()
        return jsonify(piece_urls), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, port=5004)