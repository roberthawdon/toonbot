-- MySQL dump 10.15  Distrib 10.0.25-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: toonbot
-- ------------------------------------------------------
-- Server version	10.0.25-MariaDB-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tbl_announcements`
--

DROP TABLE IF EXISTS `tbl_announcements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_announcements` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `sender` varchar(50) NOT NULL,
  `message` text NOT NULL,
  `level` tinyint(1) DEFAULT NULL,
  `sent` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_announcements`
--

LOCK TABLES `tbl_announcements` WRITE;
/*!40000 ALTER TABLE `tbl_announcements` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_announcements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_comic_data`
--

DROP TABLE IF EXISTS `tbl_comic_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_comic_data` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `comichash` varchar(50) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `text` varchar(255) DEFAULT NULL,
  `pageurl` varchar(255) DEFAULT NULL,
  `fetchtime` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `comichash` (`comichash`),
  KEY `idx_comichash` (`comichash`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_comic_data`
--

LOCK TABLES `tbl_comic_data` WRITE;
/*!40000 ALTER TABLE `tbl_comic_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_comic_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_comics`
--

DROP TABLE IF EXISTS `tbl_comics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_comics` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `comicname` varchar(50) NOT NULL,
  `displayname` varchar(50) NOT NULL,
  `latest` varchar(50) DEFAULT NULL,
  `fetch_timeout` int(4) DEFAULT NULL,
  `lastfetched` datetime DEFAULT NULL,
  `mode` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `comicname` (`comicname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_comics`
--

LOCK TABLES `tbl_comics` WRITE;
/*!40000 ALTER TABLE `tbl_comics` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_comics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_feedback`
--

DROP TABLE IF EXISTS `tbl_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_feedback` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `slackuser` varchar(50) NOT NULL,
  `message` text NOT NULL,
  `sent` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_feedback`
--

LOCK TABLES `tbl_feedback` WRITE;
/*!40000 ALTER TABLE `tbl_feedback` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_feedback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_migrations`
--

DROP TABLE IF EXISTS `tbl_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_migrations` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `migration` varchar(18) NOT NULL,
  `run` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `migration` (`migration`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_migrations`
--

LOCK TABLES `tbl_migrations` WRITE;
/*!40000 ALTER TABLE `tbl_migrations` DISABLE KEYS */;
INSERT INTO `tbl_migrations` VALUES (1,'20160413231214.sql',1),(2,'20160515162039.sql',1),(3,'20160515174722.sql',1),(4,'20160526212754.sql',1),(5,'20160528163159.sql',1),(6,'20160530165758.sql',1),(7,'20160604142654.sql',1),(8,'20160604172127.sql',1),(9,'20160629193439.sql',1),(10,'20160630213531.sql',1),(11,'20160701194209.sql',1),(12,'20160701210354.sql',1),(13,'20160702223018.sql',1),(14,'20160709201658.sql',1),(15,'20160731220943.sql',1),(16,'20160812222819.sql',1),(17,'20160815200706.sql',1),(18,'20160822220548.sql',1);
/*!40000 ALTER TABLE `tbl_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_queue`
--

DROP TABLE IF EXISTS `tbl_queue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_queue` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `slackuser` varchar(50) NOT NULL,
  `displayname` varchar(50) NOT NULL,
  `comichash` varchar(50) NOT NULL,
  `flags` tinyint(1) DEFAULT '0',
  `errormessage` varchar(50) DEFAULT NULL,
  `sent` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  KEY `tbl_queue_ibfk_1` (`slackuser`),
  KEY `tbl_queue_ibfk_2` (`comichash`),
  KEY `idx_sent` (`sent`),
  CONSTRAINT `tbl_queue_ibfk_1` FOREIGN KEY (`slackuser`) REFERENCES `tbl_users` (`slackuser`) ON UPDATE CASCADE,
  CONSTRAINT `tbl_queue_ibfk_2` FOREIGN KEY (`comichash`) REFERENCES `tbl_comic_data` (`comichash`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_queue`
--

LOCK TABLES `tbl_queue` WRITE;
/*!40000 ALTER TABLE `tbl_queue` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_queue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_queue_errors`
--

DROP TABLE IF EXISTS `tbl_queue_errors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_queue_errors` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `queueID` int(11) NOT NULL,
  `errormessage` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_queue_errors`
--

LOCK TABLES `tbl_queue_errors` WRITE;
/*!40000 ALTER TABLE `tbl_queue_errors` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_queue_errors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_subscriptions`
--

DROP TABLE IF EXISTS `tbl_subscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_subscriptions` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `slackuser` varchar(50) NOT NULL,
  `comicname` varchar(50) NOT NULL,
  `lastsent` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `idx_slackuser` (`slackuser`),
  KEY `comicname` (`comicname`),
  CONSTRAINT `tbl_subscriptions_ibfk_1` FOREIGN KEY (`slackuser`) REFERENCES `tbl_users` (`slackuser`) ON UPDATE CASCADE,
  CONSTRAINT `tbl_subscriptions_ibfk_2` FOREIGN KEY (`comicname`) REFERENCES `tbl_comics` (`comicname`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_subscriptions`
--

LOCK TABLES `tbl_subscriptions` WRITE;
/*!40000 ALTER TABLE `tbl_subscriptions` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_subscriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_system`
--

DROP TABLE IF EXISTS `tbl_system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_system` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `name` (`name`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_system`
--

LOCK TABLES `tbl_system` WRITE;
/*!40000 ALTER TABLE `tbl_system` DISABLE KEYS */;
INSERT INTO `tbl_system` VALUES (1,'db_version','1.3'),(2,'db_latest_migration','20160822220548.sql'),(3,'tb_daystart','09:00:00'),(4,'tb_dayend','17:30:00'),(5,'postcolor','DADAFF'),(6,'posttextcolor','FF8800'),(7,'fetch_timeout','10'),(8,'janitor_run','02:05:30'),(9,'bot_user',NULL);
/*!40000 ALTER TABLE `tbl_system` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_user_prefs`
--

DROP TABLE IF EXISTS `tbl_user_prefs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_user_prefs` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `slackuser` varchar(50) NOT NULL,
  `announcelevel` tinyint(1) DEFAULT NULL,
  `daystart` varchar(50) DEFAULT NULL,
  `dayend` varchar(50) DEFAULT NULL,
  `days` tinyint(3) DEFAULT NULL,
  `postcolor` varchar(6) DEFAULT NULL,
  `posttextcolor` varchar(6) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `slackuser` (`slackuser`),
  CONSTRAINT `tbl_announcement_prefs_ibfk_1` FOREIGN KEY (`slackuser`) REFERENCES `tbl_users` (`slackuser`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_user_prefs`
--

LOCK TABLES `tbl_user_prefs` WRITE;
/*!40000 ALTER TABLE `tbl_user_prefs` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_user_prefs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_users`
--

DROP TABLE IF EXISTS `tbl_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_users` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `slackuser` varchar(50) NOT NULL,
  `dmid` varchar(50) DEFAULT NULL,
  `tzoffset` int(5) DEFAULT NULL,
  `admin` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `slackuser` (`slackuser`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_users`
--

LOCK TABLES `tbl_users` WRITE;
/*!40000 ALTER TABLE `tbl_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'toonbot'
--
/*!50003 DROP PROCEDURE IF EXISTS `delete_comic` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`toonbot`@`localhost` PROCEDURE `delete_comic`(IN p_comicname VARCHAR(50))
BEGIN
    DELETE FROM tbl_subscriptions WHERE comicname = p_comicname;
    DELETE FROM tbl_comics WHERE comicname = p_comicname;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `delete_user` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`toonbot`@`localhost` PROCEDURE `delete_user`(IN p_slack_user VARCHAR(50))
BEGIN
    DELETE FROM tbl_subscriptions WHERE slackuser = p_slack_user;
    DELETE FROM tbl_user_prefs WHERE slackuser = p_slack_user;
    DELETE FROM tbl_users WHERE slackuser = p_slack_user;
    DELETE FROM tbl_queue WHERE slackuser = p_slack_user;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `make_admin` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`toonbot`@`localhost` PROCEDURE `make_admin`(IN p_slack_user VARCHAR(50))
BEGIN
    UPDATE tbl_users SET admin = 1 WHERE slackuser = p_slack_user;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-08-22 22:07:42
