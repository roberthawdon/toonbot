from __main__ import *
import MySQLdb
import time
import hashlib
import random
import urllib2
import re
from BeautifulSoup import BeautifulSoup

crontable = []
crontable.append([3600, "update_data"])
outputs = []

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

comictitle = "XKCD"
comicname = "xkcd"

try:
    conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
    curs = conn.cursor()
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

        url = 'http://xkcd.com/'

        headers = { 'User-Agent' : 'Toonbot/1.0' }

        req = urllib2.Request(url, None, headers)

        site = urllib2.urlopen(req, timeout=10).read()

        soup = BeautifulSoup(site)

        title = (soup.find("div", attrs={'id':'ctitle'})).next

        try:
            div = (soup.find("div", attrs={'id':'comic'}))

            comic = "http:" + (div.find("img")["src"])

            text = div.find("img")["title"]

            prehash = comic

        except Exception, e:

            comic = "*Today's XKCD looks to be an interactive comic.*"

            text = "_Please follow the link below to view it on the website._"

            prehash = url

        hash = hashlib.md5()
        hash.update(prehash)

        comichash = hash.hexdigest()

        permlinkextract = (soup.body.findAll(text=re.compile('Permanent link to this comic')))
        linktxt = re.search("(?P<url>https?://[^\s]+)", permlinkextract[0]).group("url")

        link = linktxt

    except Exception, e:
        return

    try:
        conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
        curs = conn.cursor()
        cmd = "SELECT comichash FROM tbl_comic_data WHERE comichash = %s"
        curs.execute(cmd, ([comichash]))
        result = curs.fetchall()
        if len(result) == 0:
            cmd = "INSERT INTO tbl_comic_data (comichash, title, image, text, pageurl) VALUES (%s, %s, %s, %s, %s)"
            curs.execute(cmd, ([comichash], [title], [comic], [text], [link]))
            cmd = "UPDATE tbl_comics SET latest = %s WHERE comicname = %s"
            curs.execute(cmd, ([comichash], [comicname]))
            conn.commit()

    except curs.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if curs:
            curs.close()
