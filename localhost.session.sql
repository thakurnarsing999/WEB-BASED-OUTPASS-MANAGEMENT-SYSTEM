CREATE DATABASE IF NOT EXISTS outpass_system;
USE outpass_system;

DROP TABLE IF EXISTS security_logs;
DROP TABLE IF EXISTS outpass_requests;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS mentors;
DROP TABLE IF EXISTS security_users;

CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    department VARCHAR(100) DEFAULT 'CSE',
    year VARCHAR(50) DEFAULT '1st Year'
);

CREATE TABLE admins (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20) NOT NULL
);

CREATE TABLE mentors (
    mentor_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    staff_id VARCHAR(50) NOT NULL UNIQUE,
    phone_no VARCHAR(20) NOT NULL
);

CREATE TABLE security_users (
    security_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20) NOT NULL
);

CREATE TABLE outpass_requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    reason VARCHAR(255) NOT NULL,
    out_date DATE NOT NULL,
    out_time TIME NOT NULL,
    parent_contact VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    otp VARCHAR(10),
    mentor_remarks VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    approved_at TIMESTAMP NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE security_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    request_id INT NOT NULL,
    otp VARCHAR(10) NOT NULL,
    verification_status VARCHAR(50) NOT NULL,
    exit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES outpass_requests(request_id) ON DELETE CASCADE
);

-- Seed values with phone_no and pre-calculated hashes (for 'admin123', 'mentor123', 'security123')
INSERT INTO admins (name, email, password, phone_no)
VALUES ('Admin User', 'admin@outpass.com', 'scrypt:32768:8:1$WE67O2NFaCtgqnAO$86de032ca9f46b08582ad5f12c68719c6820640bb6830a607fad83935e7750755ad16029b985fc02023127c6540d2ee521c21eeb62be0ef9bfd3afccf3d08247', '9999999999');

INSERT INTO mentors (name, email, password, staff_id, phone_no)
VALUES ('Mentor User', 'mentor@outpass.com', 'scrypt:32768:8:1$1RBksRhQBGbRKvL5$63c07a5743f446aaaefa5ebcc428cbfbbe18adf1622d19495c07fcafd55aa9536dc816cf999aca8de5dd0f1ddbb9958564e89f41f928b719b0f9cc7d57901728', 'MNT001', '8888888888');

INSERT INTO security_users (name, email, password, phone_no)
VALUES ('Security Guard', 'security@outpass.com', 'scrypt:32768:8:1$LFvfHJjACN56S1jl$9809c8b1d2580434ab995322b82b2b72f4588532f8845915a3e6bd5dfee17e4a2cbecc184d877daa85e8f5c47fff50c76cfad3c3ee93a1e3976d19661f511942', '7777777777');

