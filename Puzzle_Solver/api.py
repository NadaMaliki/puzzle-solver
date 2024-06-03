from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_image_path(fragment_id):
    conn = sqlite3.connect('puzzle2.db')
    cursor = conn.cursor()
    
    try:
        # Récupérer image_complete_id de la table Images9Pieces
        cursor.execute('SELECT image_complete_id FROM Images9Pieces WHERE id = ?', (fragment_id,))
        image_complete_id = cursor.fetchone()[0]
        
        # Vérifier que image_complete_id est dans image_puzzle et récupérer le chemin
        cursor.execute('SELECT chemin FROM image_puzzle WHERE image_complete_id = ?', (image_complete_id,))
        image_path = cursor.fetchone()[0]

        return image_path

    except Exception as e:
        print(f"Erreur : {e}")
        return None
    
    finally:
        conn.close()

@app.route('/hint', methods=['POST'])
def hint():
    data = request.json
    fragment_id = data.get('fragment_id')
    
    if not fragment_id:
        return jsonify({'error': 'fragment_id is required'}), 400
    
    image_path = get_image_path(fragment_id)
    
    if image_path:
        return jsonify({'image_path': image_path}), 200
    else:
        return jsonify({'error': 'Image path not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
