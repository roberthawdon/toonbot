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

* Creates new user preference table
* Transfers existing prefences to new table

*/

DROP TABLE IF EXISTS `tbl_preferences`;
CREATE TABLE `tbl_preferences` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `userpref` (`userID`, `name`),
  INDEX idx_userID (`userID`),
  INDEX idx_name (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO tbl_preferences (userID, name, value)
SELECT U.ID, "daystart", P.daystart FROM tbl_users AS U JOIN tbl_user_prefs AS P ON P.slackuser = U.slackuser WHERE P.daystart IS NOT NULL;

INSERT INTO tbl_preferences (userID, name, value)
SELECT U.ID, "dayend", P.dayend FROM tbl_users AS U JOIN tbl_user_prefs AS P ON P.slackuser = U.slackuser WHERE P.dayend IS NOT NULL;

INSERT INTO tbl_preferences (userID, name, value)
SELECT U.ID, "postcolor", P.postcolor FROM tbl_users AS U JOIN tbl_user_prefs AS P ON P.slackuser = U.slackuser WHERE P.postcolor IS NOT NULL;

INSERT INTO tbl_preferences (userID, name, value)
SELECT U.ID, "posttextcolor", P.posttextcolor FROM tbl_users AS U JOIN tbl_user_prefs AS P ON P.slackuser = U.slackuser WHERE P.posttextcolor IS NOT NULL;


