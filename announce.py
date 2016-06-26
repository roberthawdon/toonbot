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
        cmd = "SELECT A.sender, A.message, A.level, U.dmid FROM `toonbot`.`tbl_announcements` A LEFT JOIN `toonbot`.`tbl_users` U ON A.sender = U.slackuser WHERE A.sent = 0"
        curs.execute(cmd)
        result = curs.fetchall()
        if len(result) != 0:
            for messages in result:
                user = messages[0]
                message = messages[1]
                level = messages[2]
                dmid = messages[3]
                counter = 0
                cmd = "SELECT DISTINCT U.dmid, P.announcelevel FROM tbl_users U LEFT JOIN tbl_user_prefs P ON P.slackuser = U.slackuser JOIN tbl_subscriptions S ON S.slackuser = U.slackuser WHERE P.announcelevel <= %s OR P.announcelevel IS NULL;"
                curs.execute(cmd, ([level]))
                result2 = curs.fetchall()
                if len(result2) != 0:
                    for recipients in result2:
                        recipient = recipients[0]
                        outputs.append([recipient, "*Announcement* from <@" + user + ">: " + message])
                        counter = counter + 1
                    outputs.append([dmid, "The following message was delivered to `" + str(counter) + "` user(s):\n>" + message])
                else:
                    outputs.append([dmid, "The following message was *not* delivered to anyone:\n>" + message])
                cmd = "UPDATE tbl_announcements SET sent = 1 WHERE sent = 0"
                curs.execute(cmd)
                result2 = curs.fetchall()
                conn.commit()
                time.sleep(1)
                #announcementmsgs.append(name + " said: " + message)
            #announementmsgsstring = "\r\n".join(announcementmsgs)


    except curs.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if curs:
            curs.close()
