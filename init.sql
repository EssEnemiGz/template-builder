-- Drop table if exists to ensure clean state
DROP TABLE IF EXISTS users;

-- Create users table
create table users (
    id serial primary key,
    username varchar(255) not null,
    email varchar(255) not null,
    password varchar(255) not null
);  

-- Insert initial admin user only if it doesn't exist
INSERT INTO users (username, email, password)
SELECT 'admin', 'admin@localhost.com', '1234'
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'admin@localhost.com'
);