CREATE DATABASE IF NOT EXISTS dorm_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE dorm_db;

-- ตารางผู้ใช้งาน (ผู้เช่า / แอดมิน)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'tenant'
);

-- ตารางห้องพัก (สัมพันธ์กับ users)
CREATE TABLE rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(10) NOT NULL UNIQUE,
    tenant_id INT,
    FOREIGN KEY (tenant_id) REFERENCES users(id) ON DELETE SET NULL
);

-- ตารางใบแจ้งหนี้ ค่าน้ำ-ไฟ (สัมพันธ์กับ rooms)
CREATE TABLE invoices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    water_meter FLOAT NOT NULL,
    elec_meter FLOAT NOT NULL,
    total_amount FLOAT NOT NULL,
    is_paid BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
);

-- เพิ่มข้อมูลตัวอย่าง
INSERT INTO users (username, password, role) VALUES ('admin', '1234', 'admin');
INSERT INTO users (username, password, role) VALUES ('room101', '1234', 'tenant');
INSERT INTO rooms (room_number, tenant_id) VALUES ('101', 2);