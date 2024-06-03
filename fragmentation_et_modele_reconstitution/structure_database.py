import sqlite3

def create_tables():
    conn = sqlite3.connect('puzzle2.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ImagesCompletes (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            image BLOB,
            chemin TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS image_puzzle (
            id INTEGER PRIMARY KEY,
            puzzle BLOB,
            image_complete_id INTEGER,
            chemin TEXT,
            piece_order TEXT,
            FOREIGN KEY (image_complete_id) REFERENCES ImagesCompletes(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Images9Pieces (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            image BLOB,
            image_complete_id INTEGER,
            piece_order TEXT,
            FOREIGN KEY (image_complete_id) REFERENCES ImagesCompletes(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Images16Pieces (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            image BLOB,
            image_complete_id INTEGER,
            FOREIGN KEY (image_complete_id) REFERENCES ImagesCompletes(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Images36Pieces (
            id INTEGER PRIMARY KEY,
            nom TEXT,
            image BLOB,
            image_complete_id INTEGER,
            FOREIGN KEY (image_complete_id) REFERENCES ImagesCompletes(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predict2 (
            id INTEGER PRIMARY KEY,
            image_puzzle_id INTEGER,
            nom_piece_1 INTEGER,
            nom_piece_2 INTEGER,
            nom_piece_3 INTEGER,
            nom_piece_4 INTEGER,
            nom_piece_5 INTEGER,
            nom_piece_6 INTEGER,
            nom_piece_7 INTEGER,
            nom_piece_8 INTEGER,
            nom_piece_9 INTEGER,
            position_piece_1 INTEGER,
            position_piece_2 INTEGER,
            position_piece_3 INTEGER,
            position_piece_4 INTEGER,
            position_piece_5 INTEGER,
            position_piece_6 INTEGER,
            position_piece_7 INTEGER,
            position_piece_8 INTEGER,
            position_piece_9 INTEGER,
            FOREIGN KEY (image_puzzle_id) REFERENCES image_puzzle(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS puzzle_pieces (
            id INTEGER PRIMARY KEY,
            ref_img INTEGER,
            piece BLOB
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
