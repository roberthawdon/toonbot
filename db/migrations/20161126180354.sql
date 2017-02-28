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

* Updated packs table
* Adding custom commands table

*/

ALTER TABLE `tbl_packs`
ADD COLUMN `UUID` varchar(36) NOT NULL AFTER `ID`,
ADD COLUMN `packdesc` text AFTER `packname`,
ADD COLUMN `packgen` tinyint(3) AFTER `packdesc`,
ADD UNIQUE KEY `UUID` (`UUID`);

DROP TABLE IF EXISTS `tbl_commands`;
CREATE TABLE `tbl_commands` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `pack` int(11) NOT NULL,
  `command` varchar(50) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `command` (`command`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

