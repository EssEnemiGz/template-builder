// Base URL for API endpoints
const API_URL = 'http://localhost:5555';

// Function to create a new user
async function createUser(userData) {
    try {
        const response = await fetch(`${API_URL}/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        return await response.json();
    } catch (error) {
        console.error('Error creating user:', error);
        return { error: 'Failed to create user' };
    }
}

// Function to update an existing user
async function updateUser(userData) {
    try {
        const response = await fetch(`${API_URL}/users`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        return await response.json();
    } catch (error) {
        console.error('Error updating user:', error);
        return { error: 'Failed to update user' };
    }
}

// Function to delete a user
async function deleteUser(userId) {
    try {
        const response = await fetch(`${API_URL}/users`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: userId })
        });
        return await response.json();
    } catch (error) {
        console.error('Error deleting user:', error);
        return { error: 'Failed to delete user' };
    }
}

// Example usage:
const newUser = {
    username: 'testuser',
    email: 'test@example.com',
    password: 'password123'
};

// Create a new user
createUser(newUser).then(response => {
    console.log('Create user response:', response);
});

// Update a user
const updatedUser = {
    username: 'updateduser',
    email: 'updated@example.com',
    password: 'newpassword123'
};

updateUser(updatedUser).then(response => {
    console.log('Update user response:', response);
});

// Delete a user
deleteUser(1).then(response => {
    console.log('Delete user response:', response);
});
