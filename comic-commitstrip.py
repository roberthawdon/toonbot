from __main__ import *
import MySQLdb
import time
import hashlib
import random
import socket
import feedparser
from BeautifulSoup import BeautifulSoup
from datetime import datetime, time, timedelta

socket.setdefaulttimeout(10)

crontable = []
crontable.append([3600, "update_data"])
outputs = []

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

comictitle = "CommitStrip"
comicname = "commitstrip"

try:
    conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
    curs = conn.cursor()
    conn.set_character_set('utf8')
    curs.execute('SET NAMES utf8;')
    curs.execute('SET CHARACTER SET utf8;')
    curs.execute('SET character_set_connection=utf8;')
    cmd = "SELECT comicname FROM tbl_comics WHERE comicname = %s"
    curs.execute(cmd, ([comicname]))
    result = curs.fetchall()
    if len(result) == 0:
        cmd = "INSERT INTO tbl_comics (comicname, displayname) VALUES (%s, %s)"
        curs.execute(cmd, ([comicname], [comictitle]))
        conn.commit()

except curs.Error, e:

    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:

    if curs:
        curs.close()

def update_data():

    try:

        feed = feedparser.parse('http://www.commitstrip.com/en/feed/')

        result = feed.entries[0].content[0]

        soup = BeautifulSoup(result['value'])

        comic = (soup.find("img")["src"])

        title = feed.entries[0].title

        link = feed.entries[0].link

        prehash = comic

        hash = hashlib.md5()
        hash.update(prehash)

        comichash = hash.hexdigest()

    except Exception, e:
        print e
        return

    try:
        conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
        curs = conn.cursor()
        conn.set_character_set('utf8')
        curs.execute('SET NAMES utf8;')
        curs.execute('SET CHARACTER SET utf8;')
        curs.execute('SET character_set_connection=utf8;')
        cmd = "SELECT comichash FROM tbl_comic_data WHERE comichash = %s"
        curs.execute(cmd, ([comichash]))
        result = curs.fetchall()
        if len(result) == 0:
            cmd = "INSERT INTO tbl_comic_data (comichash, image, pageurl, title) VALUES (%s, %s, %s, %s)"
            curs.execute(cmd, ([comichash], [comic], [link], [title]))
            cmd = "UPDATE tbl_comics SET latest = %s WHERE comicname = %s"
            curs.execute(cmd, ([comichash], [comicname]))
            conn.commit()

    except curs.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if curs:
            curs.close()
