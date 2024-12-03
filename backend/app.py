from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
import os
import re

app = Flask(__name__)
CORS(app, resources={
    r"/users": {
        "origins": ["http://127.0.0.1:5555", "http://localhost:5555"]
    }
})

load_dotenv()

def get_db_connection():
    """
    Creates and returns a connection to the PostgreSQL database.
    """
    try:
        print(os.getenv("DB_PASSWORD"))
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'postgres'),  # Use 'postgres' as service name
            database=os.getenv('POSTGRES_DB', 'backend_db'),
            user=os.getenv('POSTGRES_USER', 'admin@localhost.com'),
            password=os.getenv('DB_PASSWORD')
        )
        return conn
    except psycopg2.Error as e:
        print(f"Unable to connect to database: {e}")
        return None

def validate_email(email):
    """
    Validates an email address using regex pattern matching.
    
    Args:
        email (str): The email address to validate
        
    Returns:
        bool: True if email is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_user_data(data, require_id=False):
    """
    Validates user data for creation or update operations.
    
    Args:
        data (dict): Dictionary containing user data
        require_id (bool): Whether to require an ID field (for updates)
        
    Returns:
        tuple: (bool, str) - (is_valid, error_message)
    """
    if not data:
        return False, "No data provided"
        
    required_fields = ['username', 'email', 'password']
    if require_id:
        required_fields.append('id')
        
    for field in required_fields:
        if field not in data:
            return False, f"Missing {field}"
            
    if len(data['username']) < 3:
        return False, "Username must be at least 3 characters long"
        
    if not validate_email(data['email']):
        return False, "Invalid email format"
        
    if len(data['password']) < 6:
        return False, "Password must be at least 6 characters long"
        
    return True, None

@app.route('/')
def hello_world():
    """Renders the index page."""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Renders the dashboard page."""
    return render_template('dashboard.html')

@app.route('/users', methods=['GET'])
def get_users():
    """
    Retrieves all users from the database.
    
    Returns:
        JSON response with list of users or error message
    """
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    try:
        cur = conn.cursor()
        cur.execute('SELECT id, username, email FROM users;')
        users = cur.fetchall()
        
        user_list = []
        for user in users:
            user_list.append({
                'id': user[0],
                'username': user[1],
                'email': user[2]
            })
            
        return jsonify({'users': user_list})
        
    except psycopg2.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/users', methods=['POST'])
def add_user():
    """
    Creates a new user in the database.
    
    Request body must contain:
        username (str): User's username (min 3 chars)
        email (str): User's email address
        password (str): User's password (min 6 chars)
        
    Returns:
        JSON response with user ID on success or error message on failure
    """
    data = request.get_json()
    
    # Validate input data
    is_valid, error_message = validate_user_data(data)
    if not is_valid:
        return jsonify({'error': error_message}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    try:
        cur = conn.cursor()
        
        # Check if email already exists
        cur.execute('SELECT id FROM users WHERE email = %s', (data['email'],))
        if cur.fetchone():
            return jsonify({'error': 'Email already exists'}), 400
        
        cur.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s) RETURNING id;',
                    (data['username'], data['email'], data['password']))
        user_id = cur.fetchone()[0]
        
        conn.commit()
        return jsonify({'id': user_id, 'message': 'User created successfully'}), 201
        
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/users', methods=['PUT'])
def update_user():
    """
    Updates an existing user's information.
    
    Request body must contain:
        id (int): User's ID
        username (str): Updated username (min 3 chars)
        email (str): Updated email address
        password (str): Updated password (min 6 chars)
        
    Returns:
        JSON response with success or error message
    """
    data = request.get_json()
    
    # Validate input data
    is_valid, error_message = validate_user_data(data, require_id=True)
    if not is_valid:
        return jsonify({'error': error_message}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    try:
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute('SELECT id FROM users WHERE id = %s', (data['id'],))
        if not cur.fetchone():
            return jsonify({'error': 'User not found'}), 404
        
        cur.execute('UPDATE users SET username=%s, email=%s, password=%s WHERE id=%s;',
                    (data['username'], data['email'], data['password'], data['id']))
        
        conn.commit()
        return jsonify({'message': 'User updated successfully'})
        
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

@app.route('/users', methods=['DELETE'])
def delete_user():
    """
    Deletes a user from the database.
    
    Request body must contain:
        id (int): ID of the user to delete
        
    Returns:
        JSON response with success or error message
    """
    data = request.get_json()
    
    # Validate input data
    if not data or 'id' not in data:
        return jsonify({'error': 'User ID is required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
        
    try:
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute('SELECT id FROM users WHERE id = %s', (data['id'],))
        if not cur.fetchone():
            return jsonify({'error': 'User not found'}), 404
        
        cur.execute('DELETE FROM users WHERE id=%s;', (data['id'],))
        
        conn.commit()
        return jsonify({'message': 'User deleted successfully'})
        
    except psycopg2.Error as e:
        conn.rollback()
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)