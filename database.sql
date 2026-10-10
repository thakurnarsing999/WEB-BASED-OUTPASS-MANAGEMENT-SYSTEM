-- ==========================================================
-- WEB-BASED OUTPASS MANAGEMENT SYSTEM
-- PostgreSQL Schema (Compatible with Supabase SQL Editor)
-- ==========================================================

-- 1. Drop existing tables if they exist
DROP TABLE IF EXISTS security_logs CASCADE;
DROP TABLE IF EXISTS outpass_requests CASCADE;
DROP TABLE IF EXISTS students CASCADE;
DROP TABLE IF EXISTS admins CASCADE;
DROP TABLE IF EXISTS mentors CASCADE;
DROP TABLE IF EXISTS security_users CASCADE;

-- 2. Create Students Table
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    roll_no VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20) NOT NULL,
    department VARCHAR(100) DEFAULT 'CSE',
    year VARCHAR(50) DEFAULT '1st Year'
);

-- 3. Create Admins Table
CREATE TABLE admins (
    admin_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20) NOT NULL
);

-- 4. Create Mentors Table
CREATE TABLE mentors (
    mentor_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    staff_id VARCHAR(50) NOT NULL UNIQUE,
    phone_no VARCHAR(20) NOT NULL
);

-- 5. Create Security Users Table
CREATE TABLE security_users (
    security_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone_no VARCHAR(20) NOT NULL
);

-- 6. Create Outpass Requests Table
CREATE TABLE outpass_requests (
    request_id SERIAL PRIMARY KEY,
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

-- 7. Create Security Exit Logs Table
CREATE TABLE security_logs (
    log_id SERIAL PRIMARY KEY,
    request_id INT NOT NULL,
    otp VARCHAR(10) NOT NULL,
    verification_status VARCHAR(50) NOT NULL,
    exit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES outpass_requests(request_id) ON DELETE CASCADE
);

