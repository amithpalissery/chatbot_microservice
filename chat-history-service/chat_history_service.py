import sqlite3
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
# Use an environment variable for the database path, allowing Docker Compose to manage it
DATABASE = os.environ.get('DATABASE_PATH', '/app/chat_history.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Initialize the database on startup
init_db()

@app.route('/healthz')
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route('/history', methods=['POST'])
def add_message():
    data = request.json
    user_id = data.get('user_id')
    role = data.get('role')
    content = data.get('content')

    if not all([user_id, role, content]):
        return jsonify({'error': 'Missing data'}), 400

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)',
                       (user_id, role, content))
        conn.commit()
    return jsonify({'status': 'Message saved'}), 201

@app.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT role, content FROM messages WHERE user_id = ? ORDER BY timestamp ASC', (user_id,))
        messages = [dict(row) for row in cursor.fetchall()]
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
