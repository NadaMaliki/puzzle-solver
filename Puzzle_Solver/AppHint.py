from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import logging

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

logging.basicConfig(level=logging.DEBUG)

def get_db_connection():
    conn = sqlite3.connect('puzzle2.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/getHint/<int:selectedPieceId>', methods=['GET'])
def get_hint(selectedPieceId):
    app.logger.debug('Request received for piece_id: %s', selectedPieceId)
    try:
        conn = get_db_connection()
        hint = conn.execute('''
            SELECT piece_order 
            FROM Images9Pieces 
            WHERE id = ? AND image_complete_id = (
                SELECT image_complete_id 
                FROM Images9Pieces 
                WHERE id = ?
            )
        ''', (selectedPieceId, selectedPieceId)).fetchone()
        conn.close()

        if hint is None:
            app.logger.debug('No hint found for piece_id: %s', selectedPieceId)
            return jsonify({'error': 'No hint found'}), 404

        app.logger.debug('Hint found: %s', hint['piece_order'])
        return jsonify({'correct_position': hint['piece_order']})
    except Exception as e:
        app.logger.error('Error occurred: %s', e)
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(port=5008)
