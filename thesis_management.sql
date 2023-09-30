-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 29, 2023 at 05:30 PM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `thesis_management`
--

-- --------------------------------------------------------

--
-- Table structure for table `advisor`
--

DROP TABLE IF EXISTS `advisor`;
CREATE TABLE IF NOT EXISTS `advisor` (
  `advisor_code` varchar(20) DEFAULT NULL,
  `institution` varchar(20) DEFAULT NULL,
  `person_id` int NOT NULL,
  `advisor_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`advisor_id`),
  KEY `R_46` (`person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `advisor`
--

INSERT INTO `advisor` (`advisor_code`, `institution`, `person_id`, `advisor_id`) VALUES
('1008', 'UNT', 8, 1);

-- --------------------------------------------------------

--
-- Table structure for table `author`
--

DROP TABLE IF EXISTS `author`;
CREATE TABLE IF NOT EXISTS `author` (
  `student_code` varchar(20) DEFAULT NULL,
  `author_id` int NOT NULL AUTO_INCREMENT,
  `person_id` int NOT NULL,
  PRIMARY KEY (`author_id`),
  KEY `R_45` (`person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `author`
--

INSERT INTO `author` (`student_code`, `author_id`, `person_id`) VALUES
('11111', 1, 2),
('1212', 3, 4),
('1000', 4, 5),
('12345678', 5, 6);

-- --------------------------------------------------------

--
-- Table structure for table `author_advisor`
--

DROP TABLE IF EXISTS `author_advisor`;
CREATE TABLE IF NOT EXISTS `author_advisor` (
  `author_id` int NOT NULL,
  `advisor_id` int NOT NULL,
  PRIMARY KEY (`advisor_id`,`author_id`),
  KEY `R_48` (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `author_reviewer`
--

DROP TABLE IF EXISTS `author_reviewer`;
CREATE TABLE IF NOT EXISTS `author_reviewer` (
  `author_id` int NOT NULL,
  `reviewer_id` int NOT NULL,
  PRIMARY KEY (`reviewer_id`,`author_id`),
  KEY `R_50` (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `author_thesis`
--

DROP TABLE IF EXISTS `author_thesis`;
CREATE TABLE IF NOT EXISTS `author_thesis` (
  `author_id` int NOT NULL,
  `thesis_id` int NOT NULL,
  PRIMARY KEY (`author_id`,`thesis_id`),
  KEY `R_58` (`thesis_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `author_thesis`
--

INSERT INTO `author_thesis` (`author_id`, `thesis_id`) VALUES
(3, 1);

-- --------------------------------------------------------

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
CREATE TABLE IF NOT EXISTS `comment` (
  `comment_id` int NOT NULL AUTO_INCREMENT,
  `comment` longtext,
  PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `comment_review`
--

DROP TABLE IF EXISTS `comment_review`;
CREATE TABLE IF NOT EXISTS `comment_review` (
  `comment_id` int NOT NULL,
  `review_id` int NOT NULL,
  PRIMARY KEY (`comment_id`,`review_id`),
  KEY `R_21` (`review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
CREATE TABLE IF NOT EXISTS `permission` (
  `permission_id` int NOT NULL AUTO_INCREMENT,
  `permission` varchar(20) DEFAULT NULL,
  `description` varchar(70) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`permission_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `permission`
--

INSERT INTO `permission` (`permission_id`, `permission`, `description`, `is_deleted`) VALUES
(1, 'test1', 'Lorem!', 0),
(2, 'test2', 'Lorem!', 0);

-- --------------------------------------------------------

--
-- Table structure for table `permission_role`
--

DROP TABLE IF EXISTS `permission_role`;
CREATE TABLE IF NOT EXISTS `permission_role` (
  `permission_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`permission_id`,`role_id`),
  KEY `R_57` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
CREATE TABLE IF NOT EXISTS `person` (
  `person_id` int NOT NULL AUTO_INCREMENT,
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `person`
--

INSERT INTO `person` (`person_id`, `firstname`, `lastname`, `phone`, `address`, `email`, `is_deleted`) VALUES
(1, 'Diego Alejandro', 'Marino Ramos', '970501313', 'Calle...', 'dmarino@unitru.edu.pe', 0),
(2, 'John', 'Doe', '999 777 555', '', 'Jon@gmail.com', 0),
(4, 'Leandro Felipe', 'Montoya Lujano', '(661) 435-9786', '37857 53rd St E, Palmdale, CA 93552-3811', 'leandromontoya@yahoo.com', 0),
(5, 'Prueba', 'Test', '100100100', '', 'test@gmail.com', 0),
(6, 'Juan', 'Perez', '91213123', '', 'jperez@gmail.com', 0),
(7, 'test1', 'test1', '999 777 555', 'Calle XYZ', 'test1@email.com', 0),
(8, 'test123', 'test321', '987654321', 'Calle dfam', 'test123@email.com', 0);

-- --------------------------------------------------------

--
-- Table structure for table `recommendation`
--

DROP TABLE IF EXISTS `recommendation`;
CREATE TABLE IF NOT EXISTS `recommendation` (
  `recommendation_id` int NOT NULL AUTO_INCREMENT,
  `recommendation_date` date DEFAULT NULL,
  `recommendation_text` longtext,
  `thesis_id` int NOT NULL,
  `advisor_id` int DEFAULT NULL,
  PRIMARY KEY (`recommendation_id`),
  KEY `R_25` (`thesis_id`),
  KEY `R_52` (`advisor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
CREATE TABLE IF NOT EXISTS `review` (
  `review_id` int NOT NULL AUTO_INCREMENT,
  `thesis_id` int NOT NULL,
  `review_date` date DEFAULT NULL,
  `rating` int DEFAULT NULL,
  `reviewer_id` int DEFAULT NULL,
  PRIMARY KEY (`review_id`),
  KEY `R_22` (`thesis_id`),
  KEY `R_53` (`reviewer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `reviewer`
--

DROP TABLE IF EXISTS `reviewer`;
CREATE TABLE IF NOT EXISTS `reviewer` (
  `reviewer_code` varchar(20) DEFAULT NULL,
  `grade` char(2) DEFAULT NULL,
  `person_id` int DEFAULT NULL,
  `reviewer_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`reviewer_id`),
  KEY `R_47` (`person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `reviewer`
--

INSERT INTO `reviewer` (`reviewer_code`, `grade`, `person_id`, `reviewer_id`) VALUES
('1000', 'DR', 7, 1);

-- --------------------------------------------------------

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
CREATE TABLE IF NOT EXISTS `role` (
  `role_id` int NOT NULL AUTO_INCREMENT,
  `role` varchar(20) DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `role`
--

INSERT INTO `role` (`role_id`, `role`, `is_deleted`) VALUES
(1, 'ADMIN', 0),
(2, 'AUTHOR', 0),
(3, 'REVIEWER', 0),
(4, 'ADVISOR', 0);

-- --------------------------------------------------------

--
-- Table structure for table `role_user`
--

DROP TABLE IF EXISTS `role_user`;
CREATE TABLE IF NOT EXISTS `role_user` (
  `user_id` int NOT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `R_55` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `role_user`
--

INSERT INTO `role_user` (`user_id`, `role_id`) VALUES
(1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `thesis`
--

DROP TABLE IF EXISTS `thesis`;
CREATE TABLE IF NOT EXISTS `thesis` (
  `thesis_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `abstract` longtext,
  `submission_date` date DEFAULT NULL,
  `thesis_status_id` int DEFAULT NULL,
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`thesis_id`),
  KEY `R_18` (`thesis_status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `thesis`
--

INSERT INTO `thesis` (`thesis_id`, `title`, `abstract`, `submission_date`, `thesis_status_id`, `is_deleted`) VALUES
(1, 'Implementacion de Software', 'Lorem', '2023-09-15', 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `thesis_status`
--

DROP TABLE IF EXISTS `thesis_status`;
CREATE TABLE IF NOT EXISTS `thesis_status` (
  `thesis_status_id` int NOT NULL AUTO_INCREMENT,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`thesis_status_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `thesis_status`
--

INSERT INTO `thesis_status` (`thesis_status_id`, `status`) VALUES
(1, 'En proceso'),
(2, 'Aprobado'),
(3, 'Rechazado'),
(4, 'En revision');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(107) DEFAULT NULL,
  `person_id` int NOT NULL,
  PRIMARY KEY (`user_id`),
  KEY `R_38` (`person_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `username`, `password`, `person_id`) VALUES
(1, 'dmarino', 'pbkdf2:sha256:600000$R1Atgo6sr40eY2hY$85586c02cfa96acc1bbbc01bb3e8a4bc2d77be46ba737b62e3e513978aa924e3', 1),
(2, 'scars 2 success', 'pbkdf2:sha256:600000$R1Atgo6sr40eY2hY$85586c02cfa96acc1bbbc01bb3e8a4bc2d77be46ba737b62e3e513978aa924e3', 4);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `advisor`
--
ALTER TABLE `advisor`
  ADD CONSTRAINT `R_46` FOREIGN KEY (`person_id`) REFERENCES `person` (`person_id`);

--
-- Constraints for table `author`
--
ALTER TABLE `author`
  ADD CONSTRAINT `R_45` FOREIGN KEY (`person_id`) REFERENCES `person` (`person_id`);

--
-- Constraints for table `author_advisor`
--
ALTER TABLE `author_advisor`
  ADD CONSTRAINT `R_48` FOREIGN KEY (`author_id`) REFERENCES `author` (`author_id`),
  ADD CONSTRAINT `R_49` FOREIGN KEY (`advisor_id`) REFERENCES `advisor` (`advisor_id`);

--
-- Constraints for table `author_reviewer`
--
ALTER TABLE `author_reviewer`
  ADD CONSTRAINT `R_50` FOREIGN KEY (`author_id`) REFERENCES `author` (`author_id`),
  ADD CONSTRAINT `R_51` FOREIGN KEY (`reviewer_id`) REFERENCES `reviewer` (`reviewer_id`);

--
-- Constraints for table `author_thesis`
--
ALTER TABLE `author_thesis`
  ADD CONSTRAINT `R_16` FOREIGN KEY (`author_id`) REFERENCES `author` (`author_id`),
  ADD CONSTRAINT `R_58` FOREIGN KEY (`thesis_id`) REFERENCES `thesis` (`thesis_id`);

--
-- Constraints for table `comment_review`
--
ALTER TABLE `comment_review`
  ADD CONSTRAINT `R_20` FOREIGN KEY (`comment_id`) REFERENCES `comment` (`comment_id`),
  ADD CONSTRAINT `R_21` FOREIGN KEY (`review_id`) REFERENCES `review` (`review_id`);

--
-- Constraints for table `permission_role`
--
ALTER TABLE `permission_role`
  ADD CONSTRAINT `R_56` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`permission_id`),
  ADD CONSTRAINT `R_57` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`);

--
-- Constraints for table `recommendation`
--
ALTER TABLE `recommendation`
  ADD CONSTRAINT `R_25` FOREIGN KEY (`thesis_id`) REFERENCES `thesis` (`thesis_id`),
  ADD CONSTRAINT `R_52` FOREIGN KEY (`advisor_id`) REFERENCES `advisor` (`advisor_id`);

--
-- Constraints for table `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `R_22` FOREIGN KEY (`thesis_id`) REFERENCES `thesis` (`thesis_id`),
  ADD CONSTRAINT `R_53` FOREIGN KEY (`reviewer_id`) REFERENCES `reviewer` (`reviewer_id`);

--
-- Constraints for table `reviewer`
--
ALTER TABLE `reviewer`
  ADD CONSTRAINT `R_47` FOREIGN KEY (`person_id`) REFERENCES `person` (`person_id`);

--
-- Constraints for table `role_user`
--
ALTER TABLE `role_user`
  ADD CONSTRAINT `R_54` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`),
  ADD CONSTRAINT `R_55` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`);

--
-- Constraints for table `thesis`
--
ALTER TABLE `thesis`
  ADD CONSTRAINT `R_18` FOREIGN KEY (`thesis_status_id`) REFERENCES `thesis_status` (`thesis_status_id`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `R_38` FOREIGN KEY (`person_id`) REFERENCES `person` (`person_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
