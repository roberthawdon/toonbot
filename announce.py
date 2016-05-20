from __main__ import *
import MySQLdb
import time
import hashlib
import random
import json
import urllib2

crontable = []
crontable.append([60, "post_announcements"])

outputs = []

slacktoken = config["SLACK_TOKEN"]

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

def post_announcements():
    try:
        conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
        curs = conn.cursor()
        conn.set_character_set('utf8')
        curs.execute('SET NAMES utf8;')
        curs.execute('SET CHARACTER SET utf8;')
        curs.execute('SET character_set_connection=utf8;')
        cmd = "SELECT sender, message, level FROM tbl_announcements WHERE sent = 0"
        curs.execute(cmd)
        result = curs.fetchall()
        if len(result) != 0:
            for messages in result:
                user = messages[0]
                message = messages[1]
                level = messages[2]
                cmd = "SELECT U.dmid, P.level FROM tbl_users U LEFT JOIN tbl_announcement_prefs P ON P.slackuser = U.slackuser WHERE P.level <= %s OR P.level IS NULL;"
                curs.execute(cmd, ([level]))
                result2 = curs.fetchall()
                for recipients in result2:
                    recipient = recipients[0]
                    outputs.append([recipient, "*Announcement* from <@" + user + ">: " + message])
                cmd = "UPDATE tbl_announcements SET sent = 1 WHERE sent = 0"
                curs.execute(cmd)
                result2 = curs.fetchall()
                conn.commit()
                #announcementmsgs.append(name + " said: " + message)
            #announementmsgsstring = "\r\n".join(announcementmsgs)


    except curs.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if curs:
            curs.close()
