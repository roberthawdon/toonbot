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

* Fixing delete_user stored procedure

*/

DROP PROCEDURE IF EXISTS `delete_user`;
DELIMITER ;;
CREATE DEFINER=`toonbot`@`localhost` PROCEDURE `delete_user`(IN p_slack_user VARCHAR(50))
BEGIN
DELETE FROM tbl_queue WHERE slackuser = p_slack_user;
DELETE FROM tbl_subscriptions WHERE slackuser = p_slack_user;
DELETE FROM tbl_user_prefs WHERE slackuser = p_slack_user;
DELETE FROM tbl_users WHERE slackuser = p_slack_user;
END ;;
DELIMITER ;
