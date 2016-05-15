from __main__ import *
import MySQLdb
import time
import hashlib
import random
import urllib2
from BeautifulSoup import BeautifulSoup

posttime = random.randint(180,600)

crontable = []
crontable.append([3600, "update_data"])
crontable.append([posttime, "post_comic"])
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

        link = url

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

def post_comic():
    try:
        conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
        curs = conn.cursor()
        cmd = "SELECT latest FROM tbl_comics WHERE comicname = %s"
        curs.execute(cmd, ([comicname]))
        result = curs.fetchall()
        for hash in result:
            currenthash = hash[0]

        cmd = "SELECT image, pageurl, title, text FROM tbl_comic_data WHERE comichash = %s"
        curs.execute(cmd, ([currenthash]))
        result = curs.fetchall()
        for comicdata in result:
            image = comicdata[0]
            pageurl = comicdata[1]
            title = comicdata[2]
            text = comicdata[3]

        cmd = "SELECT U.slackuser, U.dmid, S.lastsent FROM tbl_subscriptions S LEFT OUTER JOIN tbl_users U ON U.slackuser = S.slackuser WHERE comicname = %s"
        curs.execute(cmd, ([comicname]))
        result = curs.fetchall()
        for subscribed in result:
            if subscribed[2] != currenthash:
                outputs.append([subscribed[1], "*" + comictitle + "*\n_" + title + "_\n" + image])
                outputs.append([subscribed[1], "> " + text + "\n```" + pageurl + "```"])
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
