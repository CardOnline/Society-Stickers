
from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__)

db_path = 'database.db'


# Initialize Database
def init_db():
    if not os.path.exists(
            db_path):  # Ensure the database is created only if missing
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            flat_number TEXT NOT NULL,
                            name TEXT NOT NULL,
                            mobile TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS qr_scans (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            qr_code TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS payments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            utr_number TEXT NOT NULL)''')
        conn.commit()
        conn.close()
        print("Database initialized successfully.")


# Serve Frontend (index.html and other static files)
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)


# Register User
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or 'flatNumber' not in data or 'name' not in data or 'mobile' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (flat_number, name, mobile) VALUES (?, ?, ?)",
        (data['flatNumber'], data['name'], data['mobile']))
    conn.commit()
    conn.close()
    return jsonify({"message": "User registered successfully!"})


# Scan QR Code
@app.route('/scan_qr', methods=['POST'])
def scan_qr():
    data = request.get_json()
    if not data or 'qrCode' not in data:
        return jsonify({"error": "QR Code missing"}), 400

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO qr_scans (qr_code) VALUES (?)",
                   (data['qrCode'], ))
    conn.commit()
    conn.close()
    return jsonify({"message": "QR Code Scanned Successfully!"})


# Submit Payment
@app.route('/submit_payment', methods=['POST'])
def submit_payment():
    data = request.get_json()
    if not data or 'utrNumber' not in data:
        return jsonify({"error": "Transaction ID missing"}), 400

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO payments (utr_number) VALUES (?)",
                   (data['utrNumber'], ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Payment Recorded Successfully!"})


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
