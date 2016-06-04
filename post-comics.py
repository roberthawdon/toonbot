from __main__ import *
import MySQLdb
import random
from checktime import workhourscheck

posttime = random.randint(180, 600)

crontable = []
crontable.append([posttime, "post_comics"])
outputs = []

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

try:
    conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
    curs = conn.cursor()
    cmd = "SELECT name, value FROM tbl_system WHERE name = %s"
    curs.execute(cmd, ["tb_daystart"])
    result = curs.fetchall()
    for starttime in result:
        defaultstart = starttime[1]
    curs.execute(cmd, ["tb_dayend"])
    result = curs.fetchall()
    for endtime in result:
        defaultend = endtime[1]

except curs.Error, e:

    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:

    if curs:
        curs.close()

def post_comics():
    try:
        comicname = []

        image = None
        pageurl = None
        title = None
        text = None

        conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
        curs = conn.cursor()
        conn.set_character_set('utf8')
        curs.execute('SET NAMES utf8;')
        curs.execute('SET CHARACTER SET utf8;')
        curs.execute('SET character_set_connection=utf8;')
        cmd = "SELECT comicname FROM tbl_comics"
        curs.execute(cmd)
        comicresult = curs.fetchall()

        for selectedcomic in comicresult:
            comicrun = selectedcomic[0]
            cmd = "SELECT latest, displayname FROM tbl_comics WHERE comicname = %s"
            curs.execute(cmd, ([selectedcomic]))
            result = curs.fetchall()
            for comiclist in result:
                currenthash = comiclist[0]
                displayname = comiclist[1]

            if currenthash:
                cmd = "SELECT image, pageurl, title, text FROM tbl_comic_data WHERE comichash = %s"
                curs.execute(cmd, ([currenthash]))
                result = curs.fetchall()
                for comicdata in result:
                    image = comicdata[0]
                    pageurl = comicdata[1]
                    title = comicdata[2]
                    if title:
                        utitle = title.decode("utf-8")
                        title = utitle.encode("ascii", "ignore")
                    text = comicdata[3]
                    if text:
                        utext = text.decode("utf-8")
                        text = utext.encode("ascii", "ignore")

                if title:
                    firstmsg = "*" + displayname + "*\n_" + title + "_\n" + image
                else:
                    firstmsg = "*" + displayname + "*\n" + image

                if text:
                    secondmsg = "> " + text + "\n```" + pageurl + "```"
                else:
                    secondmsg = "```" + pageurl + "```"

                cmd = "SELECT U.slackuser, U.dmid, P.daystart, P.dayend, U.tzoffset, S.lastsent FROM tbl_subscriptions S LEFT OUTER JOIN tbl_users U ON U.slackuser = S.slackuser LEFT OUTER JOIN tbl_user_prefs P ON U.slackuser = P.slackuser WHERE comicname = %s"
                curs.execute(cmd, ([comicrun]))
                result = curs.fetchall()
                for subscribed in result:
                    starttime = subscribed[2]
                    endtime = subscribed[3]
                    offset = subscribed[4]
                    if starttime is None:
                        starttime = defaultstart
                    if endtime is None:
                        endtime = defaultend
                    if offset is None:
                        offset = 0
                    if subscribed[5] != currenthash:
                        if workhourscheck(starttime, endtime, offset):
                            outputs.append([subscribed[1], firstmsg])
                            outputs.append([subscribed[1], secondmsg])
                            cmd = "UPDATE tbl_subscriptions SET lastsent = %s WHERE slackuser = %s AND comicname = %s"
                            curs.execute(cmd, ([currenthash], [subscribed[0]], [comicrun]))
                            result = curs.fetchall()
                            conn.commit()

    except curs.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if curs:
            curs.close()
