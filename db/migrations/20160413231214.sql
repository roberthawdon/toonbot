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

Important notes:

This initial migration requires a bit of manual intervention, as it creates the
system in the database to handle migrations. The migration script will fail to
run unless the tables generated in this migration already exist.

To apply this migration manually, run the following, substituting the correct
credentials where nessessary:

mysql -utoonbot -p toonbot < 20160413231214.sql

After this has been run, you must then run the migration script to tear down the
tables created, and rebuild them with the correct data in place. From then on,
migrations that have already been run should not run again.

----------

Changelog:

* Adds migration tracker
 * Adds tbl_migrations
 * Adds tbl_system
* Upgrades database from V0.9 to V1.0

*/

DROP TABLE IF EXISTS `tbl_migrations`;
CREATE TABLE `tbl_migrations` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `migration` varchar(18) NOT NULL,
  `run` tinyint(1),
  PRIMARY KEY (`ID`),
  UNIQUE KEY `migration` (`migration`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tbl_system`;
CREATE TABLE `tbl_system` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `value` varchar(255),
  PRIMARY KEY (`ID`),
  UNIQUE KEY `name` (`name`),
  INDEX idx_name (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT IGNORE INTO tbl_migrations SET migration = "20160413231214.sql";

INSERT INTO `tbl_system` (`name`, `value`) VALUES ('db_version', '1.0'), ('db_latest_migration', NULL);
