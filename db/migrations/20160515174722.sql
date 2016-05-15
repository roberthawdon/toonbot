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

* Adds comic display name data

*/

UPDATE tbl_comics SET displayname = "Andy Capp" WHERE comicname = "andy-capp";
UPDATE tbl_comics SET displayname = "Calvin and Hobbes" WHERE comicname = "calvin-and-hobbes";
UPDATE tbl_comics SET displayname = "Cyanide and Happiness" WHERE comicname = "cyanide-and-happiness";
UPDATE tbl_comics SET displayname = "Dilbert" WHERE comicname = "dilbert";
UPDATE tbl_comics SET displayname = "Garfield" WHERE comicname = "garfield";
UPDATE tbl_comics SET displayname = "Peanuts" WHERE comicname = "peanuts";
UPDATE tbl_comics SET displayname = "Penny Arcade" WHERE comicname = "penny-arcade";
UPDATE tbl_comics SET displayname = "Perry Bible Fellowship" WHERE comicname = "perry-bible-fellowship";
UPDATE tbl_comics SET displayname = "Tales Of Mere Existence" WHERE comicname = "tales-of-mere-existence";
UPDATE tbl_comics SET displayname = "U.S. Acres" WHERE comicname = "us-acres";
UPDATE tbl_comics SET displayname = "XKCD" WHERE comicname = "xkcd";
