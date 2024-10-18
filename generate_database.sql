-- 1. Create the database
CREATE DATABASE IF NOT EXISTS my_database;

-- 2. Use the newly created database
USE my_database;

-- 3. Create the User table
CREATE TABLE User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    profile VARCHAR(255),  -- Assuming this will store a file path or URL for the profile picture
    name VARCHAR(100) NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    role ENUM('Admin', 'User', 'Moderator') NOT NULL,  -- Customizable roles
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    address TEXT
);

-- 4. Create the Category table
CREATE TABLE Category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- 5. Create the Product table
CREATE TABLE Product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(50) NOT NULL,
    image VARCHAR(255),  -- Assuming this will store a file path or URL for the product image
    name VARCHAR(100) NOT NULL,
    category_id INT,
    cost DECIMAL(10, 2) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    current_stock INT NOT NULL,
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES Category(id) ON DELETE SET NULL
);

-- 6. Add indexes to optimize queries
-- CREATE INDEX idx_user_email ON User(email);
-- CREATE INDEX idx_product_code ON Product(code);
