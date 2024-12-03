// Base URL for API endpoints
const API_URL = 'http://127.0.0.1:5555';

// Function to create a new user
async function createUser() {
    const userData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    try {
        const response = await fetch(`${API_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        const result = await response.json();
        console.log('Create user response:', result);
        
        if (result.error) {
            alert(result.error);
        } else {
            alert('User created successfully!');
            clearForm();
        }
    } catch (error) {
        console.error('Error creating user:', error);
        alert('Failed to create user');
    }
}

// Function to update an existing user
async function updateUser() {
    const userId = document.getElementById('userId').value;
    if (!userId) {
        alert('Please enter a user ID to update');
        return;
    }

    const userData = {
        id: parseInt(userId),
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    try {
        const response = await fetch(`${API_URL}/users`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        const result = await response.json();
        console.log('Update user response:', result);
        
        if (result.error) {
            alert(result.error);
        } else {
            alert('User updated successfully!');
            clearForm();
        }
    } catch (error) {
        console.error('Error updating user:', error);
        alert('Failed to update user');
    }
}

// Function to delete a user
async function deleteUser() {
    const userId = document.getElementById('userId').value;
    if (!userId) {
        alert('Please enter a user ID to delete');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/users`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: parseInt(userId) })
        });
        const result = await response.json();
        console.log('Delete user response:', result);
        
        if (result.error) {
            alert(result.error);
        } else {
            alert('User deleted successfully!');
            clearForm();
        }
    } catch (error) {
        console.error('Error deleting user:', error);
        alert('Failed to delete user');
    }
}

// Helper function to clear the form
function clearForm() {
    document.getElementById('username').value = '';
    document.getElementById('email').value = '';
    document.getElementById('password').value = '';
    document.getElementById('userId').value = '';
}