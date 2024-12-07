import psycopg2
import os
import re

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
    print(data)
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
