-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.8.6-MariaDB - MariaDB Server
-- Server OS:                    Win64
-- HeidiSQL Version:             12.14.0.7165
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for dorm_db
CREATE DATABASE IF NOT EXISTS `dorm_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `dorm_db`;

-- Dumping structure for table dorm_db.invoices
CREATE TABLE IF NOT EXISTS `invoices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_id` int(11) NOT NULL,
  `water_meter` float NOT NULL,
  `elec_meter` float NOT NULL,
  `total_amount` float NOT NULL,
  `is_paid` tinyint(1) DEFAULT 0,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `room_id` (`room_id`),
  CONSTRAINT `invoices_ibfk_1` FOREIGN KEY (`room_id`) REFERENCES `rooms` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table dorm_db.invoices: ~2 rows (approximately)
INSERT INTO `invoices` (`id`, `room_id`, `water_meter`, `elec_meter`, `total_amount`, `is_paid`, `created_at`) VALUES
	(1, 1, 25, 25, 650, 0, '2026-04-07 16:35:26'),
	(2, 1, 30, 25, 740, 0, '2026-04-07 16:41:55');

-- Dumping structure for table dorm_db.repairs
CREATE TABLE IF NOT EXISTS `repairs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_number` varchar(10) NOT NULL,
  `description` text NOT NULL,
  `status` varchar(50) DEFAULT 'รอดำเนินการ',
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `room_number` (`room_number`),
  CONSTRAINT `repairs_ibfk_1` FOREIGN KEY (`room_number`) REFERENCES `rooms` (`room_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table dorm_db.repairs: ~0 rows (approximately)

-- Dumping structure for table dorm_db.rooms
CREATE TABLE IF NOT EXISTS `rooms` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `room_number` varchar(10) NOT NULL,
  `tenant_id` int(11) DEFAULT NULL,
  `tenant_name` varchar(100) DEFAULT NULL,
  `job` varchar(100) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `room_number` (`room_number`),
  KEY `tenant_id` (`tenant_id`),
  CONSTRAINT `rooms_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table dorm_db.rooms: ~11 rows (approximately)
INSERT INTO `rooms` (`id`, `room_number`, `tenant_id`, `tenant_name`, `job`, `image_url`) VALUES
	(1, '101', 2, 'นายสมชาย ใจดี', 'วิศวกร', 'https://i.pravatar.cc/150?u=101'),
	(52, '102', NULL, 'น.ส.แพรวพรรณ', 'พนักงานออฟฟิศ', 'https://i.pravatar.cc/150?u=102'),
	(53, '201', NULL, NULL, NULL, NULL),
	(57, '103', NULL, 'นายวิชัย มั่งคั่ง', 'ธุรการ', 'https://i.pravatar.cc/150?u=103'),
	(58, '104', NULL, 'น.ส.จิราพร แสนสุข', 'นักศึกษา', 'https://i.pravatar.cc/150?u=104'),
	(59, '105', NULL, 'นายธนา สวยใส', 'กราฟิกดีไซน์', 'https://i.pravatar.cc/150?u=105'),
	(60, '106', NULL, 'น.S.วรรณวิสาข์', 'ครู', 'https://i.pravatar.cc/150?u=106'),
	(61, '107', NULL, 'นายมานะ ขยันยิ่ง', 'ฟรีแลนซ์', 'https://i.pravatar.cc/150?u=107'),
	(62, '108', NULL, 'น.ส.ดวงใจ รวยรื่น', 'เจ้าของธุรกิจ', 'https://i.pravatar.cc/150?u=108'),
	(63, '109', NULL, 'นายเก่งกาจ กล้าหาญ', 'ทนายความ', 'https://i.pravatar.cc/150?u=109'),
	(64, '110', NULL, 'น.ส.นภา ฟ้าใส', 'แอร์โฮสเตส', 'https://i.pravatar.cc/150?u=110');

-- Dumping structure for table dorm_db.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` varchar(20) DEFAULT 'tenant',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- Dumping data for table dorm_db.users: ~2 rows (approximately)
INSERT INTO `users` (`id`, `username`, `password`, `role`) VALUES
	(1, 'admin', '1234', 'admin'),
	(2, 'room101', '1234', 'tenant');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
