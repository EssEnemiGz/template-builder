// Function to fetch and display users
async function fetchUsers() {
    try {
        const response = await fetch('http://localhost:5555/users');
        const data = await response.json();
        console.log(data)
        
        const tableBody = document.getElementById('userTableBody');
        tableBody.innerHTML = ''; // Clear existing content
        
        data.users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.username}</td>
                <td>${user.email}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error fetching users:', error);
    }
}

// Fetch users when page loads
document.addEventListener('DOMContentLoaded', fetchUsers);