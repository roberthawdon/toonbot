-- MySQL dump 10.15  Distrib 10.0.29-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: localhost
-- ------------------------------------------------------
-- Server version	10.0.29-MariaDB-0ubuntu0.16.04.1

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
  `text` text,
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
  `alias` varchar(50) DEFAULT NULL,
  `pack` int(11) DEFAULT NULL,
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
-- Table structure for table `tbl_commands`
--

DROP TABLE IF EXISTS `tbl_commands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_commands` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `pack` int(11) NOT NULL,
  `command` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `command` (`command`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_commands`
--

LOCK TABLES `tbl_commands` WRITE;
/*!40000 ALTER TABLE `tbl_commands` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_commands` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_custom_preferences`
--

DROP TABLE IF EXISTS `tbl_custom_preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_custom_preferences` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `default` varchar(255) DEFAULT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_custom_preferences`
--

LOCK TABLES `tbl_custom_preferences` WRITE;
/*!40000 ALTER TABLE `tbl_custom_preferences` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_custom_preferences` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_migrations`
--

LOCK TABLES `tbl_migrations` WRITE;
/*!40000 ALTER TABLE `tbl_migrations` DISABLE KEYS */;
INSERT INTO `tbl_migrations` VALUES (1,'20160413231214.sql',1),(2,'20160515162039.sql',1),(3,'20160515174722.sql',1),(4,'20160526212754.sql',1),(5,'20160528163159.sql',1),(6,'20160530165758.sql',1),(7,'20160604142654.sql',1),(8,'20160604172127.sql',1),(9,'20160629193439.sql',1),(10,'20160630213531.sql',1),(11,'20160701194209.sql',1),(12,'20160701210354.sql',1),(13,'20160702223018.sql',1),(14,'20160709201658.sql',1),(15,'20160731220943.sql',1),(16,'20160812222819.sql',1),(17,'20160815200706.sql',1),(18,'20160822220548.sql',1),(19,'20161113154226.sql',1),(20,'20161113164545.sql',1),(21,'20161118154454.sql',1),(22,'20161121190932.sql',1),(23,'20161125203030.sql',1),(24,'20161125231142.sql',1),(25,'20161126180354.sql',1),(26,'20161127182918.sql',1),(27,'20161127190826.sql',1),(28,'20161222172849.sql',1),(29,'20161223172519.sql',1),(30,'20161223181346.sql',1),(31,'20161223233743.sql',1),(32,'20161224200832.sql',1),(33,'20161224213139.sql',1),(34,'20161225013320.sql',1),(35,'20170226182938.sql',1),(36,'20170228211507.sql',1);
/*!40000 ALTER TABLE `tbl_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_packs`
--

DROP TABLE IF EXISTS `tbl_packs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_packs` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `UUID` varchar(36) NOT NULL,
  `packcode` varchar(50) NOT NULL,
  `packname` varchar(50) NOT NULL,
  `packdesc` text,
  `packgen` tinyint(3) DEFAULT NULL,
  `version` varchar(50) DEFAULT NULL,
  `directory` varchar(50) NOT NULL,
  `github` varchar(255) DEFAULT NULL,
  `autoupdate` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `packcode` (`packcode`),
  UNIQUE KEY `UUID` (`UUID`),
  UNIQUE KEY `directory` (`directory`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_packs`
--

LOCK TABLES `tbl_packs` WRITE;
/*!40000 ALTER TABLE `tbl_packs` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_packs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_preferences`
--

DROP TABLE IF EXISTS `tbl_preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tbl_preferences` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `userpref` (`userID`,`name`),
  KEY `idx_userID` (`userID`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_preferences`
--

LOCK TABLES `tbl_preferences` WRITE;
/*!40000 ALTER TABLE `tbl_preferences` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_preferences` ENABLE KEYS */;
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
INSERT INTO `tbl_system` VALUES (1,'db_version','1.4'),(2,'db_latest_migration','20170228211507.sql'),(3,'tb_daystart','09:00:00'),(4,'tb_dayend','17:30:00'),(5,'postcolor','DADAFF'),(6,'posttextcolor','FF8800'),(7,'fetch_timeout','10'),(8,'janitor_run','02:05:30'),(9,'bot_user',NULL);
/*!40000 ALTER TABLE `tbl_system` ENABLE KEYS */;
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
  `account_disabled` tinyint(1) NOT NULL DEFAULT '0',
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
/*!50003 DROP PROCEDURE IF EXISTS `delete_comic_pack` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`toonbot`@`localhost` PROCEDURE `delete_comic_pack`(IN p_packname VARCHAR(50))
BEGIN
    DELETE FROM tbl_subscriptions WHERE comicname IN (SELECT comicname FROM tbl_comics WHERE pack = (SELECT ID FROM tbl_packs WHERE packcode = p_packname));
    DELETE FROM tbl_comics WHERE pack = (SELECT ID FROM tbl_packs WHERE packcode = p_packname);
    DELETE FROM tbl_packs WHERE packcode = p_packname;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `delete_custom_preference` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = latin1 */ ;
/*!50003 SET character_set_results = latin1 */ ;
/*!50003 SET collation_connection  = latin1_swedish_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`toonbot`@`localhost` PROCEDURE `delete_custom_preference`(IN p_preference VARCHAR(255))
BEGIN
    DELETE FROM tbl_preferences WHERE name = p_preference;
    DELETE FROM tbl_custom_preferences WHERE name = p_preference;
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
DELETE FROM tbl_queue WHERE slackuser = p_slack_user;
DELETE FROM tbl_subscriptions WHERE slackuser = p_slack_user;
DELETE FROM tbl_user_prefs WHERE slackuser = p_slack_user;
DELETE FROM tbl_users WHERE slackuser = p_slack_user;
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

-- Dump completed on 2017-02-28 21:21:02
