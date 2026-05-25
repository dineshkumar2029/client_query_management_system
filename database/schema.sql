CREATE DATABASE client_query_system;

USE client_query_system;

CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL
);

CREATE TABLE queries (
    query_id INT PRIMARY KEY AUTO_INCREMENT,
    mail_id VARCHAR(100),
    mobile_number VARCHAR(20),
    query_heading VARCHAR(255),
    query_description TEXT,
    status VARCHAR(20) DEFAULT 'Open',
    query_created_time DATETIME,
    query_closed_time DATETIME
);