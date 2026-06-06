from flask import Blueprint, request, jsonify
import pyodbc
import hashlib
from config import CONNECTION_STRING

auth_bp = Blueprint('auth', __name__)

def get_db():
    return pyodbc.connect(CONNECTION_STRING)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')

    if not all([username, email, password]):
        return jsonify({'error': 'All fields required'}), 400

    conn = get_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO Users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
        """, username, email, hash_password(password), role)
        conn.commit()
        return jsonify({'message': f'User {username} registered successfully'}), 201
    except pyodbc.IntegrityError:
        return jsonify({'error': 'Username or email already exists'}), 409
    finally:
        conn.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({'error': 'Username and password required'}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, role 
        FROM Users 
        WHERE username = ? AND password_hash = ?
    """, username, hash_password(password))

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    return jsonify({
        'message': 'Login successful',
        'user_id': user[0],
        'username': user[1],
        'role': user[2]
    }), 200
