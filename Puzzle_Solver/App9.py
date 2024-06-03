from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import base64
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/api/relatedData/<int:image_id>', methods=['GET'])
def get_related_data(image_id):
    try:
        conn = sqlite3.connect('puzzle2.db')
        cursor = conn.cursor()
        
        logging.debug(f"Fetching data for image_id: {image_id}")
        
        cursor.execute('''
            SELECT Pieces.id, Pieces.image
            FROM Images9Pieces AS Pieces
            WHERE Pieces.image_complete_id = ?
        ''', (image_id+1,))
        rows = cursor.fetchall()
        
        if not rows:
            logging.warning(f"No pieces found for image_id: {image_id}")
            return jsonify({'error': 'No pieces found for the given image ID.'}), 404
        
        pieces_data = []
        for row in rows:
            piece_id = row[0]
            image_data = row[1]
            if image_data:
                base64_piece = base64.b64encode(image_data).decode('utf-8')
                piece_url = f"data:image/png;base64,{base64_piece}"
                pieces_data.append({'id': piece_id, 'url': piece_url})
            else:
                logging.warning(f"Piece with id {piece_id} has no image data.")
        
        conn.close()
        logging.debug(f"Successfully fetched {len(pieces_data)} pieces for image_id: {image_id}")
        return jsonify(pieces_data), 200
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")
        return jsonify({'error': 'Database error: ' + str(e)}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Unexpected error: ' + str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
