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

* Adding timezone column to tbl_users for future implementation of quite hours.
* Dropping unused tbl_announcement_prefs.
* Creating tbl_user_prefs.

*/

ALTER TABLE `tbl_users`
ADD COLUMN `tzoffset` int(5) AFTER `dmid`;

DROP TABLE IF EXISTS `tbl_announcement_prefs`;
CREATE TABLE `tbl_user_prefs` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `slackuser` varchar(50) NOT NULL,
  `announcelevel` tinyint(1),
  `daystart` int(5),
  `dayend` int(5),
  `days` tinyint(3),
  PRIMARY KEY (`ID`),
  UNIQUE KEY `slackuser` (`slackuser`),
  CONSTRAINT `tbl_announcement_prefs_ibfk_1` FOREIGN KEY (`slackuser`) REFERENCES `tbl_users` (`slackuser`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP PROCEDURE IF EXISTS `delete_user`;
DELIMITER ;;
CREATE DEFINER=`toonbot`@`localhost` PROCEDURE `delete_user`(IN p_slack_user VARCHAR(50))
BEGIN
    DELETE FROM tbl_subscriptions WHERE slackuser = p_slack_user;
    DELETE FROM tbl_user_prefs WHERE slackuser = p_slack_user;
    DELETE FROM tbl_users WHERE slackuser = p_slack_user;
END ;;
DELIMITER ;
