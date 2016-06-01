# Toon Bot
#
#  _____   U  ___ u   U  ___ u  _   _           ____     U  ___ u _____
# |_ " _|   \/"_ \/    \/"_ \/ | \ |"|       U | __")u    \/"_ \/|_ " _|
#   | |     | | | |    | | | |<|  \| |>       \|  _ \/    | | | |  | |
#  /| |\.-,_| |_| |.-,_| |_| |U| |\  |u        | |_) |.-,_| |_| | /| |\
# u |_|U \_)-\___/  \_)-\___/  |_| \_|         |____/  \_)-\___/ u |_|U
# _// \\_     \\         \\    ||   \\,-.     _|| \\_       \\   _// \\_
# (__) (__)   (__)       (__)   (_")  (_/     (__) (__)     (__) (__) (__)
#
#                                   Providing 5 minute breaks since 2016
#
# By Robert Hawdon - https://robertianhawdon.me.uk/

from __main__ import *
import time
import MySQLdb
import sys
import json
import urllib2
from prettytable import PrettyTable
from checktimezone import checktimezone

crontable = []
outputs = []

slacktoken = config["SLACK_TOKEN"]
botuser = config["BOT_USER"]

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

def process_message(data):
    if data['type'] == "message" and data['channel'].startswith("D") and 'subtype' not in data and data['user'] != botuser:
        try:
            conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
            curs = conn.cursor()
            cmd = "SELECT slackuser, dmid, admin FROM tbl_users WHERE slackuser = %s"
            curs.execute(cmd, ([data['user']]))
            result = curs.fetchall()
            if len(result) == 0:
                register(data, conn, curs)
            else:
                for users in result:
                    admin = users[2]
                if data['text'] == "list":
                    list(data, curs)
                elif data['text'].startswith("feedback"):
                    feedback(data, conn, curs)
                elif data['text'].startswith("announce") and str(admin) == '1':
                    announce(data, conn, curs)
                elif data['text'] == "help":
                    help(data)
                else:
                    comic_selector(data, conn, curs)

        except curs.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

        finally:

            if curs:
                curs.close()

def register(data, conn, curs):
    cmd = "INSERT INTO tbl_users (slackuser, dmid) values (%s, %s)"
    curs.execute(cmd, ([data['user']], [data['channel']]))
    conn.commit()
    checktimezone(data['user'])
    outputs.append([data['channel'], "Hello <@" + data['user'] + ">, I don't think we've met. Type `list` to show a list of available comics to get started."])

def comic_selector(data, conn, curs):
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

def help(data):
    outputs.append([data['channel'], "Type `list` to view a list of available comics. You can subscribe to a comic by sending its name. Once subscribed, you'll receive the latest comic in a few minutes. If you change your mind, you can also unsubscribe by sending its name again. The `list` command will be updated to reflect which comics you are currently subscribed to.\n I should not be added to public or private chat rooms, but in the event I am, I will not talk. I've been designed to only talk in direct messages."])

def announce(data, conn, curs):
    # TO-DO: Implement announcement levels (Issue 26)
    announcelevel = "0"
    try:
        announcemessage = data['text'].split(' ', 1)[1]
        cmd = "INSERT INTO tbl_announcements (sender, message, level) VALUES (%s, %s, %s);"
        curs.execute(cmd, ([data['user']], [announcemessage], [announcelevel]))
        conn.commit()
        outputs.append([data['channel'], "Your announcement will be broadcast shortly."])
    except Exception, e:
        outputs.append([data['channel'], "Syntax error"])

def feedback(data, conn, curs):
    try:
        feedbackmessage = data['text'].split(' ', 1)[1]
        cmd = "INSERT INTO tbl_feedback (slackuser, message) VALUES (%s, %s);"
        curs.execute(cmd, ([data['user']], [feedbackmessage]))
        conn.commit()
        outputs.append([data['channel'], "Thanks for the feedback."])
    except Exception, e:
        outputs.append([data['channel'], "Please type `feedback` followed by your message."])

def list(data, curs):
    tablecomics = PrettyTable(["Comic", "Subscribed"])
    tablecomics.align["Comic"] = "l"
    tablecomics.padding_width = 1
    cmd = "SELECT C.comicname, S.slackuser AS enabled FROM tbl_comics C LEFT JOIN tbl_subscriptions S ON S.comicname = C.comicname AND S.slackuser = %s"
    curs.execute(cmd, ([data['user']]))
    result = curs.fetchall()
    for comics in result:
        if comics[1] == data['user']:
            enabledflag = "Yes"
        else:
            enabledflag = ""
        tablecomics.add_row([comics[0], enabledflag])
    outputs.append([data['channel'], "Here is a list of available comics:\n```" + str(tablecomics) + "```\nType the name of each comic you want to subscribe to as an individual message. Type the name again to unsubscribe."])
