from __main__ import *
import MySQLdb
import feedparser
import time
import hashlib
from BeautifulSoup import BeautifulSoup
from datetime import datetime

crontable = []
crontable.append([300, "update_data"])
crontable.append([300, "post_comic"])
outputs = []

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

comictitle = "Penny Arcade"
comicname = "penny-arcade"

try:
    conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
    curs = conn.cursor()
    cmd = "SELECT comicname FROM tbl_comics WHERE comicname = %s"
    curs.execute(cmd, ([comicname]))
    result = curs.fetchall()
    if len(result) == 0:
        cmd = "INSERT INTO tbl_comics (comicname) VALUES (%s)"
        curs.execute(cmd, ([comicname]))
        conn.commit()

except curs.Error, e:

    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:

    if curs:
        curs.close()

def update_data():

    feed = feedparser.parse('http://www.comicsyndicate.org/Feed/Penny%20Arcade')

    result = feed.entries[0].summary_detail

    soup = BeautifulSoup(result['value'])

    comic = (soup.find("img")["src"])

    title = (soup.find("img")["alt"])

    link = (soup.find("a")["href"])

    prehash = comic

    hash = hashlib.md5()
    hash.update(prehash)

    comichash = hash.hexdigest()

    try:
        conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
        curs = conn.cursor()
        cmd = "SELECT comichash FROM tbl_comic_data WHERE comichash = %s"
        curs.execute(cmd, ([comichash]))
        result = curs.fetchall()
        if len(result) == 0:
            cmd = "INSERT INTO tbl_comic_data (comichash, title, image, pageurl) VALUES (%s, %s, %s, %s)"
            curs.execute(cmd, ([comichash], [title], [comic], [link]))
            cmd = "UPDATE tbl_comics SET latest = %s WHERE comicname = %s"
            curs.execute(cmd, ([comichash], [comicname]))
            conn.commit()

    except curs.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if curs:
            curs.close()

def post_comic():
    try:
        conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
        curs = conn.cursor()
        cmd = "SELECT latest FROM tbl_comics WHERE comicname = %s"
        curs.execute(cmd, ([comicname]))
        result = curs.fetchall()
        for hash in result:
            currenthash = hash[0]

        cmd = "SELECT image, pageurl, title FROM tbl_comic_data WHERE comichash = %s"
        curs.execute(cmd, ([currenthash]))
        result = curs.fetchall()
        for comicdata in result:
            image = comicdata[0]
            pageurl = comicdata[1]
            title = comicdata[2]

        cmd = "SELECT U.slackuser, U.dmid, S.lastsent FROM tbl_subscriptions S LEFT OUTER JOIN tbl_users U ON U.slackuser = S.slackuser WHERE comicname = %s"
        curs.execute(cmd, ([comicname]))
        result = curs.fetchall()
        for subscribed in result:
            if subscribed[2] != currenthash:
                outputs.append([subscribed[1], "*" + comictitle + "*\n_" + title + "_\n" + image])
                outputs.append([subscribed[1], "```" + pageurl + "```"])
                cmd = "UPDATE tbl_subscriptions SET lastsent = %s WHERE slackuser = %s AND comicname = %s"
                curs.execute(cmd, ([currenthash], [subscribed[0]], [comicname]))
                result = curs.fetchall()
                conn.commit()

    except curs.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if curs:
            curs.close()
