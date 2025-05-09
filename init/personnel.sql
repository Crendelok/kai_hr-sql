CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_department_id INT
);

CREATE TABLE positions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    department_id INT,
    salary DECIMAL(10, 2)
);

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    date_of_birth DATE,
    passport_number VARCHAR(20),
    tax_id VARCHAR(20),
    address TEXT,
    phone_number VARCHAR(20),
    email VARCHAR(100),
    hire_date DATE NOT NULL,
    position_id INT,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE employment_actions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    action_type ENUM('hire', 'transfer', 'terminate') NOT NULL,
    action_date DATE NOT NULL,
    reason TEXT,
    new_position_id INT
);

CREATE TABLE leave_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    leave_type ENUM('annual', 'sick', 'unpaid', 'maternity', 'other') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending'
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'hr', 'viewer') NOT NULL
);
