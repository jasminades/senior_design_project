from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:5173')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="detection_db"
)
cursor = db.cursor(dictionary=True)

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")
db.commit()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    
    if not full_name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
    
    try:
        cursor.execute(
            "INSERT INTO users (full_name, email, password) VALUES (%s, %s, %s)",
            (full_name, email, hashed)
        )
        db.commit()
        return jsonify({"message": "User registered successfully"})
    except mysql.connector.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    row = cursor.fetchone()
    
    if row and bcrypt.checkpw(password.encode(), row["password"].encode()):
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
