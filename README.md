Here's a comprehensive documentation for the software:

# Backend Template Documentation

## Overview
This is a Flask-based backend template with PostgreSQL database integration, containerized using Docker. The system provides basic user management functionality through a RESTful API.

## System Requirements
- Docker and Docker Compose
- Git

## Project Structure
```
.
├── backend/
│   ├── app.py              # Main Flask application
│   ├── Dockerfile          # Flask container configuration
│   ├── requirements.txt    # Python dependencies
│   └── templates/          # HTML templates
├── docker-compose.yml      # Container orchestration
├── init.sql               # Database initialization
├── .env                   # Environment variables
└── .gitignore            # Git ignore rules
```

## Setup and Installation

### 1. Installation Script
The project includes a template installation script that can be run to set up the builder:
```bash
./setup.sh
```

This script will:
- Install the template-builder to `/usr/local/bin/`
- Create a `.template-builder` directory in your home folder
- Copy template files to the installation directory

### Using the Template Builder
After installation, you can create a new project structure automatically by running:
```bash
template-builder
```
This command will:
- Create the basic project structure in your current directory
- Set up all necessary files and folders as shown in the Project Structure section
- Create basic Docker configuration files
- NOTE: Remember to create the `.env` file with the correct environment variables

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
DB_PASSWORD=your_secure_password
```
Note: Replace `your_secure_password` with a secure password.

### 3. Starting the Application
```bash
docker-compose build && docker-compose up -d
```
This will:
- Start PostgreSQL on port 5433
- Start Flask application on port 5555
- Initialize the database with the schema from `init.sql`

## Database Structure
The PostgreSQL database includes a `users` table with the following schema:
```sql
create table users (
    id serial primary key,
    username varchar(255) not null,
    email varchar(255) not null,
    password varchar(255) not null
);
```

## API Endpoints

### 1. Create User
- **Endpoint:** `POST /users`
- **Content-Type:** `application/json`
- **Request Body:**
```json
{
    "username": "string",  // minimum 3 characters
    "email": "string",     // valid email format
    "password": "string"   // minimum 6 characters
}
```
- **Response:** `201 Created` with user ID or error message

### 2. Update User
- **Endpoint:** `PUT /users`
- **Content-Type:** `application/json`
- **Request Body:**
```json
{
    "id": "integer",
    "username": "string",  // minimum 3 characters
    "email": "string",     // valid email format
    "password": "string"   // minimum 6 characters
}
```
- **Response:** `200 OK` with success message or error message

### 3. Delete User
- **Endpoint:** `DELETE /users`
- **Content-Type:** `application/json`
- **Request Body:**
```json
{
    "id": "integer"
}
```
- **Response:** `200 OK` with success message or error message

## Data Validation
The system includes validation for:
- Username (minimum 3 characters)
- Email (valid format)
- Password (minimum 6 characters)
- Duplicate email addresses

## Development Notes

### Docker Configuration
- PostgreSQL container:
  - External port: 5433
  - Internal port: 5432
  - Database name: backend_db
  - User: admin@localhost.com

- Flask container:
  - Port: 5555
  - Development mode enabled
  - Hot-reload supported through volume mounting

### Security Considerations
- Database passwords are managed through environment variables
- `.env` file is excluded from version control
- Database data is persisted using Docker volumes

### Database Connection
The application uses the following connection parameters:
```python
host: "localhost"
database: "postgres"
user: "postgres"
password: from environment variable
```

## Troubleshooting

### Common Issues
1. Template Builder Installation
   - Ensure you have sudo privileges
   - Verify ~/.template-builder directory exists after installation
   - Check file permissions on /usr/local/bin/template-builder

2. Database Connection Failures
   - Verify `.env` file exists with correct credentials
   - Ensure PostgreSQL container is running
   - Check port availability (5433)

3. API Errors
   - Check request format matches documentation
   - Verify all required fields are present
   - Ensure data meets validation requirements

### Logs Access
```bash
# View Flask logs
docker logs flask_server

# View PostgreSQL logs
docker logs bulider_template
```

## Development Setup
1. Clone the repository
2. Create and configure `.env` file
3. Run `docker-compose build && docker-compose up -d`
4. Access API at `http://localhost:5555`

The system is now ready for development and testing.
