DROP DATABASE IF EXISTS `scores`;
CREATE DATABASE `scores`; 
USE `scores`;

SET NAMES utf8 ;
SET character_set_client = utf8mb4 ;

CREATE TABLE `ranking_levels` (
  `try` int(3) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `score` int(6) NOT NULL,
  `exercise` int(2) NOT NULL,
  PRIMARY KEY (`try`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `ranking_levels` VALUES (1,STR_TO_DATE('10-03-2023','%d-%m-%Y'),300,2);
INSERT INTO `ranking_levels` VALUES (2,STR_TO_DATE('10-03-2023','%d-%m-%Y'),150,6);
INSERT INTO `ranking_levels` VALUES (3,STR_TO_DATE('10-03-2023','%d-%m-%Y'),850,7);
INSERT INTO `ranking_levels` VALUES (4,STR_TO_DATE('10-03-2023','%d-%m-%Y'),320,7);

  

CREATE TABLE `ranking_RQG` (
  `try` int(3) NOT NULL AUTO_INCREMENT,
  `date` date DEFAULT NULL,
  `score` int(6) NOT NULL,
  PRIMARY KEY (`try`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
INSERT INTO `ranking_RQG` VALUES (1,STR_TO_DATE('10-03-2023','%d-%m-%Y'),300);
INSERT INTO `ranking_RQG` VALUES (2,STR_TO_DATE('10-03-2023','%d-%m-%Y'),150);
INSERT INTO `ranking_RQG` VALUES (3,STR_TO_DATE('10-03-2023','%d-%m-%Y'),850);
INSERT INTO `ranking_RQG` VALUES (4,STR_TO_DATE('10-03-2023','%d-%m-%Y'),320);





