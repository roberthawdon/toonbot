/* Toon Bot

 _____   U  ___ u   U  ___ u  _   _           ____     U  ___ u _____
|_ " _|   \/"_ \/    \/"_ \/ | \ |"|       U | __")u    \/"_ \/|_ " _|
  | |     | | | |    | | | |<|  \| |>       \|  _ \/    | | | |  | |
 /| |\.-,_| |_| |.-,_| |_| |U| |\  |u        | |_) |.-,_| |_| | /| |\
u |_|U \_)-\___/  \_)-\___/  |_| \_|         |____/  \_)-\___/ u |_|U
_// \\_     \\         \\    ||   \\,-.     _|| \\_       \\   _// \\_
(__) (__)   (__)       (__)   (_")  (_/     (__) (__)     (__) (__) (__)

                                  Providing 5 minute breaks since 2016

Database migration file
-------- --------- ----

(C) 2016 Robert Ian Hawdon - https://robertianhawdon.me.uk/

----------

Changelog:

* Creates custom preferences table
* Creates procedure to remove custom preferences

*/

DROP TABLE IF EXISTS `tbl_custom_preferences`;
CREATE TABLE `tbl_custom_preferences` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `name` (`name`),
  CONSTRAINT `tbl_custom_preferences_ibfk_1` FOREIGN KEY (`name`) REFERENCES `tbl_preferences` (`name`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP PROCEDURE IF EXISTS `delete_custom_preference`;
DELIMITER ;;
CREATE DEFINER=`toonbot`@`localhost` PROCEDURE `delete_custom_preference`(IN p_preference VARCHAR(255))
BEGIN
    DELETE FROM tbl_preferences WHERE name = p_preference;
    DELETE FROM tbl_custom_preferences WHERE name = p_preference;
END ;;
DELIMITER ;
