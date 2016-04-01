from __main__ import *
import time
import MySQLdb
import sys
import json
import urllib2
from prettytable import PrettyTable

crontable = []
outputs = []

slacktoken = config["SLACK_TOKEN"]
botuser = config["BOT_USER"]

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]



def process_message(data):
    #print data
    if data['type'] == "message" and data['channel'].startswith("D") and 'subtype' not in data and data['user'] != botuser:
        try:
            conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
            curs = conn.cursor()
            cmd = "SELECT * FROM tbl_users WHERE slackuser = %s"
            curs.execute(cmd, ([data['user']]))
            result = curs.fetchall()
            if len(result) == 0:
                req = "https://slack.com/api/im.list?token=" + slacktoken
                response = urllib2.urlopen(req)
                jsonres = json.load(response)
                dmid = []
                slackuser = []
                for dms in jsonres["ims"]:
                    dmid.append(dms["id"])
                    slackuser.append(dms["user"])
                indexid = slackuser.index(data['user'])
                dchannelid = dmid[indexid]
                cmd = "INSERT INTO tbl_users (slackuser, dmid) values (%s, %s)"
                curs.execute(cmd, ([data['user']], [dchannelid]))
                conn.commit()
                outputs.append([data['channel'], "Hello <@" + data['user'] + ">, I don't think we've met. Type `list` to show a list of available comics to get started."])
            else:
                if data['text'] == "list":
                    tablecomics = PrettyTable(["Comic", "Subscribed"])
                    tablecomics.align["Comic"] = "l"
                    tablecomics.padding_width = 1
                    cmd = "SELECT C.comicname, S.slackuser AS enabled FROM tbl_comics C LEFT JOIN tbl_subscriptions S ON S.comicname = C.comicname AND S.slackuser = %s"
                    curs.execute(cmd, ([data['user']]))
                    result = curs.fetchall()
                    #comiclist = []
                    for comics in result:
                        if comics[1] == data['user']:
                            enabledflag = "Yes"
                        else:
                            enabledflag = ""
                        tablecomics.add_row([comics[0], enabledflag])
                    outputs.append([data['channel'], "Here is a list of available comics:\n```" + str(tablecomics) + "```\nType the name of each comic you want to subscribe to as an individual message. Type the name again to unsubscribe."])
                elif data['text'].startswith("feedback"):
                    outputs.append([data['channel'], "Sorry, the feedback function is still being worked on."])
                elif data['text'] == "help":
                    outputs.append([data['channel'], "Type `list` to view a list of available comics. You can subscribe to a comic by sending its name. Once subscribed, you'll receive the latest comic in a few minutes. If you change your mind, you can also unsubscribe by sending its name again. The `list` command will be updated to reflect which comics you are currently subscribed to.\n I should not be added to public or private chat rooms, but in the event I am, I will not talk. I've been designed to only talk in direct messages."])
                else:
                    cmd = "SELECT * FROM tbl_comics WHERE comicname = %s"
                    curs.execute(cmd, ([data['text']]))
                    result = curs.fetchall()
                    if len(result) == 0:
                        outputs.append([data['channel'], "Sorry, I don't have a comic called `" + data['text'] + "` in my database."])
                    else:
                        cmd = "SELECT * FROM tbl_subscriptions WHERE comicname = %s AND slackuser = %s"
                        curs.execute(cmd, ([data['text'], [data['user']]]))
                        result = curs.fetchall()
                        if len(result) == 0:
                            cmd = "INSERT INTO tbl_subscriptions (comicname, slackuser) VALUES (%s, %s)"
                            curs.execute(cmd, ([data['text'], [data['user']]]))
                            conn.commit()
                            result = curs.fetchall()
                            outputs.append([data['channel'], "You are now subscribed to `" + data['text'] + "`."])
                        else:
                            cmd = "DELETE FROM tbl_subscriptions WHERE comicname = %s AND slackuser = %s"
                            curs.execute(cmd, ([data['text'], [data['user']]]))
                            conn.commit()
                            result = curs.fetchall()
                            outputs.append([data['channel'], "You are now unsubscribed from `" + data['text'] + "`."])

        except curs.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

        finally:

            if curs:
                curs.close()
