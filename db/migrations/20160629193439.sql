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

* Adding queue table for queueing up posts.
* Rewrote delete_user stored procedure to allow removal of user if they have comics queued.
* Upgrade database version to v1.1.

*/

CREATE TABLE `tbl_queue` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `slackuser` varchar(50) NOT NULL,
  `displayname` varchar(50) NOT NULL,
  `comichash` varchar(50) NOT NULL,
  `flags` tinyint(1) DEFAULT 0,
  PRIMARY KEY (`ID`),
  CONSTRAINT `tbl_queue_ibfk_1` FOREIGN KEY (`slackuser`) REFERENCES `tbl_users` (`slackuser`) ON UPDATE CASCADE,
  CONSTRAINT `tbl_queue_ibfk_2` FOREIGN KEY (`comichash`) REFERENCES `tbl_comic_data` (`comichash`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP PROCEDURE IF EXISTS `delete_user`;
DELIMITER ;;
CREATE DEFINER=`toonbot`@`localhost` PROCEDURE `delete_user`(IN p_slack_user VARCHAR(50))
BEGIN
    DELETE FROM tbl_subscriptions WHERE slackuser = p_slack_user;
    DELETE FROM tbl_user_prefs WHERE slackuser = p_slack_user;
    DELETE FROM tbl_users WHERE slackuser = p_slack_user;
    DELETE FROM tbl_queue WHERE slackuser = p_slack_user;
END ;;
DELIMITER ;

UPDATE `tbl_system` SET `value` = '1.1' WHERE `name` = 'db_version';
