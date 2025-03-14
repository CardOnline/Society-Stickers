from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import os
import re  # ✅ Import regex module for extracting UTR and Amount

app = Flask(__name__)
db_path = 'database.db'


# Initialize Database (Creates missing tables without deleting data)
def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ensure all tables exist
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

    # ✅ Updated: Added amount field
    cursor.execute('''CREATE TABLE IF NOT EXISTS sms_reports (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sender TEXT NOT NULL,
                        sms_text TEXT NOT NULL,
                        utr_number TEXT,
                        amount TEXT)''')
    
     # ✅ Check if 'amount' column exists; if not, add it
    cursor.execute("PRAGMA table_info(sms_reports)")
    columns = [row[1] for row in cursor.fetchall()]
    if "amount" not in columns:
        cursor.execute("ALTER TABLE sms_reports ADD COLUMN amount TEXT")
        print("✅ Added 'amount' column to sms_reports table.")

    conn.commit()
    conn.close()
    print("Database checked and updated successfully.")


# Function to extract UTR and Amount from SMS
def extract_utr_and_amount(sms_text):
    """Extracts UTR and Amount from the given SMS text"""
    
    # ✅ Extract UTR (12+ digit number)
    utr_match = re.search(r'\b\d{12,}\b', sms_text)
    utr_number = utr_match.group() if utr_match else None

    # ✅ Extract Amount (₹, Rs, or numbers with decimals)
    # amount_match = re.search(r'(?i)(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d{1,2})?)', sms_text)
    amount_match = re.search(r'(?i)(?:₹|Rs\.?|INR)\s*([\d,]+(?:\.\d{1,2})?)', sms_text)
    
    amount = amount_match.group(1) if amount_match else None

    return utr_number, amount


# Submit SMS and Extract UTR + Amount
@app.route('/submit_sms', methods=['POST'])
def submit_sms():
    data = request.get_json()
    sender = data.get('sender')
    sms_text = data.get('sms_text')

    if not sender or not sms_text:
        return jsonify({"error": "Sender and SMS text are required!"}), 400

    # ✅ Extract UTR and Amount
    utr_number, amount = extract_utr_and_amount(sms_text)

    # Store SMS data in SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sms_reports (sender, sms_text, utr_number, amount) VALUES (?, ?, ?, ?)",
                   (sender, sms_text, utr_number, amount))
    conn.commit()
    conn.close()

    return jsonify({
        "message": "SMS stored successfully!",
        "utr_number": utr_number,
        "amount": amount
    })


# Serve Frontend (index.html and other static files)
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)


if __name__ == '__main__':
    init_db()  # ✅ Ensures all tables are created
    app.run(host='0.0.0.0', port=5000)
