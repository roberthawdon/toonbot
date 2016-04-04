from __main__ import *
import MySQLdb
import time
import hashlib
import random
import smtplib
import json
import urllib2
from prettytable import PrettyTable

crontable = []
crontable.append([3600, "post_feedback"])

slacktoken = config["SLACK_TOKEN"]

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

mailto = config["FEEDBACK_TO"]
smtpserver = config["SMTP_SERVER"]
smtpport = config["SMTP_PORT"]
smtpuser = config["SMTP_USER"]
smtppass = config["SMTP_PASS"]

def post_feedback():
    try:
        conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
        curs = conn.cursor()
        cmd = "SELECT slackuser, message FROM tbl_feedback WHERE sent = 0"
        curs.execute(cmd)
        result = curs.fetchall()
        if len(result) != 0:
            feedbacktable = PrettyTable(["Name", "Message"])
            #feedbackmsgs = []
            for messages in result:
                user = messages[0]
                message = messages[1]
                try:
                    req = "https://slack.com/api/users.info?token=" + slacktoken +"&user=" + user
                    response = urllib2.urlopen(req)
                    slackname = json.load(response)
                    if slackname["user"]["real_name"] != "":
                        name = slackname["user"]["real_name"]
                    else:
                        name = slackname["user"]["name"]
                except Exception, e:
                    print "Error getting slack user name: " + str(e)
                    return
                feedbacktable.add_row([name, message])
                #feedbackmsgs.append(name + " said: " + message)
            #feedbackmsgsstring = "\r\n".join(feedbackmsgs)

            msg = "\r\n".join([
              "From: " + smtpuser + "",
              "To: " + mailto + "",
              "Subject: [Toonbot] Feedback received",
              "",
              "Hello,",
              "",
              "You have received the following feedback messages from users of Toonbot:",
              "",
              str(feedbacktable),
              "",
              "Regards,",
              "  Toonbot",
              ])

            server = smtplib.SMTP(smtpserver + ':' + smtpport)
            server.ehlo()
            server.starttls()
            server.login(smtpuser,smtppass)
            server.sendmail(smtpuser, mailto, msg)
            server.quit()

            cmd = "UPDATE tbl_feedback SET sent = 1 WHERE sent = 0"
            curs.execute(cmd)
            result = curs.fetchall()
            conn.commit()

    except curs.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if curs:
            curs.close()
