"""
Render users info.
By: EssEnemiGz
"""

from flask import jsonify, request, Blueprint
import common.networking as networking
import psycopg2

render_bp = Blueprint("render", __name__)

@render_bp.route('/users', methods=['GET'])
def get_users():
    """
    Retrieves all users from the database.
    
    Returns:
        JSON response with list of users or error message
    """
    conn = networking.get_db_connection()
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

@render_bp.route('/users', methods=['POST'])
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
    is_valid, error_message = networking.validate_user_data(data)
    if not is_valid:
        return jsonify({'error': error_message}), 400
    
    conn = networking.get_db_connection()
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

@render_bp.route('/users', methods=['PUT'])
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
    is_valid, error_message = networking.validate_user_data(data, require_id=True)
    if not is_valid:
        return jsonify({'error': error_message}), 400
    
    conn = networking.get_db_connection()
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

@render_bp.route('/users', methods=['DELETE'])
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
    
    conn = networking.get_db_connection()
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