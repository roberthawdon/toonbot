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
import re
import os
from datetime import datetime
from checktimezone import checktimezone

# Lobby Modules
script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))
lobby_dirpath = script_dirpath + '/lobby'
sys.path.insert(0, lobby_dirpath)

from reference import *
from admin_management import *
from comic_selector import *
from feedback_set import *
from admin_announce import *
from user_prefs import *

crontable = []
outputs = []

slacktoken = config["SLACK_TOKEN"]
botuser = config["BOT_USER"]

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

if 'FEEDBACK' in config:
    if config["FEEDBACK"]:
        feedbacksetting = True
    else:
        feedbacksetting = False
else:
    feedbacksetting = True

botversion = "0.7.0-dev"
botcodename = "Project Lulu"

def process_message(data):
    lobby = None
    if data['type'] == "message" and data['channel'].startswith("D") and 'subtype' not in data and data['user'] != botuser:
        data['text'] = data['text'].encode('utf8')
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
                    lobby = list(data, curs)
                elif data['text'].startswith("feedback") and feedbacksetting:
                    lobby = feedback(data, conn, curs)
                elif data['text'].startswith("announce") and str(admin) == '1':
                    lobby = announce(data, conn, curs)
                elif data['text'].startswith("makeadmin") and str(admin) == '1':
                    lobby = promoteadmin(data, conn, curs)
                elif data['text'].startswith("revokeadmin") and str(admin) == '1':
                    lobby = revokeadmin(data, conn, curs)
                elif data['text'] == "claimadmin":
                    lobby = claimadmin(data, conn, curs, admin)
                elif data['text'] == "help":
                    lobby = help(data)
                elif data['text'] == "about":
                    lobby = about(data)
                elif data['text'].startswith("start"):
                    lobby = setstarttime(data, conn, curs)
                elif data['text'].startswith("end"):
                    lobby = setendtime(data, conn, curs)
                elif data['text'].startswith("postcolour") or data['text'].startswith("postcolor"):
                    lobby = setpostcolour(data, conn, curs)
                elif data['text'].startswith("posttextcolour") or data['text'].startswith("posttextcolour"):
                    lobby = setposttextcolour(data, conn, curs)
                elif data['text'] == "clear preferences":
                    lobby = resetprefs(data, conn, curs)
                elif data['text'] == "show preferences":
                    lobby = showprefs(data, conn, curs)
                elif data['text'] == "version":
                    lobby = showversion(data, curs, botversion, botcodename)
                else:
                    lobby = comic_selector(data, conn, curs)

                if lobby is not None:
                    outputs.append(lobby[0])
                    del lobby[:]
                else:
                    outputs.append([data['channel'], "Something went wrong with the lobby module that deals with this command and I was not given anything to say."])


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
