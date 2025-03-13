from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

db_path = 'database.db'

def init_db():
    if not os.path.exists(db_path):  # Ensure the database is created only if missing
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            flat_number TEXT NOT NULL,
                            name TEXT NOT NULL,
                            mobile TEXT NOT NULL)
                        ''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS qr_scans (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            qr_code TEXT NOT NULL)
                        ''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            utr_number TEXT NOT NULL)
                        ''')
        conn.commit()
        conn.close()
        print("Database initialized successfully.")

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (flat_number, name, mobile) VALUES (?, ?, ?)",
                   (data['flatNumber'], data['name'], data['mobile']))
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered successfully!"})

@app.route('/scan_qr', methods=['POST'])
def scan_qr():
    data = request.json
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO qr_scans (qr_code) VALUES (?)", (data['qrCode'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "QR Code Scanned Successfully!"})

@app.route('/submit_payment', methods=['POST'])
def submit_payment():
    data = request.json
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO payments (utr_number) VALUES (?)", (data['utrNumber'],))
    conn.commit()
    conn.close()
    return jsonify({"message": "Payment Recorded Successfully!"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)