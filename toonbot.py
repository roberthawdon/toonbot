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
#   Copyright (C) 2016  Robert Ian Hawdon - https://robertianhawdon.me.uk
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __main__ import *
import time
import MySQLdb
import sys
import json
import urllib2
import re
import os
from datetime import datetime
from checkaccount import checkaccount
from botuser import getbotuser
from rtmbot.core import Plugin
from confload import ToonbotConf

config = ToonbotConf()

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
from admin_comics import *
from admin_system import *

slacktoken = config["SLACK_TOKEN"]

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

def register(data, conn, curs):
    outputs = []
    cmd = "INSERT INTO tbl_users (slackuser, dmid) values (%s, %s)"
    curs.execute(cmd, ([data['user']], [data['channel']]))
    conn.commit()
    checkaccount(data['user'])
    outputs.append([data['channel'], "Hello <@" + data['user'] + ">, I don't think we've met. Type `list` to show a list of available comics to get started."])
    return outputs

class ToonBot(Plugin):


    if 'FEEDBACK' in config:
        if config["FEEDBACK"]:
            feedbacksetting = True
        else:
            feedbacksetting = False
    else:
        feedbacksetting = True

    botversion = "0.8.0"
    botcodename = "Garfield"

    try:
        conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
        curs = conn.cursor()
        cmd = "SELECT value FROM tbl_system WHERE name = 'bot_user'"
        curs.execute(cmd)
        result = curs.fetchall()
        if len(result) == 0:
            botuser = getbotuser()
            cmd = "INSERT IGNORE INTO tbl_system (name, value) VALUES ('bot_user', %s)"
            curs.execute(cmd, ([botuser]))
            conn.commit()
        else:
            for botusers in result:
                botuser = botusers[0]
            checkbotuser = getbotuser()
            if checkbotuser != botuser:
                botuser = checkbotuser
                cmd = "INSERT IGNORE INTO tbl_system (name, value) VALUES ('bot_user', %s) ON DUPLICATE KEY UPDATE value = %s"
                curs.execute(cmd, ([botuser], [botuser]))
                conn.commit()
        curs.close()

    except curs.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        print "Error checking my user details."
        sys.exit(1)

    def process_message(self, data):
        ## Uncomment the line below to get a raw dump of the Slack data printed on the terminal
        # print data
        lobby = None
        if data['type'] == "message" and data['channel'].startswith("D") and 'subtype' not in data and data['user'] != self.botuser:
            data['text'] = data['text'].encode('utf8')
            try:
                conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
                curs = conn.cursor()
                cmd = "SELECT slackuser, dmid, admin FROM tbl_users WHERE slackuser = %s"
                curs.execute(cmd, ([data['user']]))
                result = curs.fetchall()
                if len(result) == 0:
                    lobby = register(data, conn, curs)
                else:
                    for users in result:
                        admin = users[2]
                    if data['text'] == "list":
                        lobby = list(data, curs)
                    elif data['text'].startswith("feedback") and self.feedbacksetting:
                        lobby = feedback(data, conn, curs)
                    elif data['text'].startswith("announce") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = announce(data, conn, curs)
                    elif data['text'].startswith("makeadmin") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = promoteadmin(data, conn, curs, self.botuser)
                    elif data['text'].startswith("revokeadmin") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = revokeadmin(data, conn, curs, self.botuser)
                    elif data['text'].startswith("makesuperadmin") and str(admin) == '2':
                        lobby = promotesuperadmin(data, conn, curs, self.botuser)
                    elif data['text'].startswith("revokesuperadmin") and str(admin) == '2':
                        lobby = revokesuperadmin(data, conn, curs, self.botuser)
                    elif data['text'].startswith("comicadmin") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = comicadmin(data, conn, curs)
                    elif data['text'] == "claimadmin":
                        lobby = claimadmin(data, conn, curs, admin)
                    elif data['text'] == "claimsuperadmin" and (str(admin) == '1' or str(admin) == '2'):
                        lobby = claimsuperadmin(data, conn, curs, admin)
                    elif data['text'].startswith("globalstart") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = globalstarttime(data, conn, curs)
                    elif data['text'].startswith("globalend") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = globalendtime(data, conn, curs)
                    elif data['text'].startswith("globalpostcolour") or data['text'].startswith("globalpostcolor") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = globalpostcolor(data, conn, curs)
                    elif data['text'].startswith("globalposttextcolour") or data['text'].startswith("globalposttextcolor") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = globalposttextcolor(data, conn, curs)
                    elif data['text'].startswith("fetchtimeout") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = comicfetchtimeout(data, conn, curs)
                    elif data['text'].startswith("janitortime") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = janitorruntime(data, conn, curs)
                    elif data['text'].startswith("deletepack") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = deletepack(data, conn, curs)
                    elif data['text'].startswith("installpack") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = installpack(data, conn, curs)
                    elif data['text'].startswith("updatepack") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = updatepack(data, conn, curs)
                    elif data['text'].startswith("packadmin") and (str(admin) == '1' or str(admin) == '2'):
                        lobby = packadmin(data, conn, curs)
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
                        lobby = showversion(data, curs, self.botversion, self.botcodename)
                    else:
                        lobby = comic_selector(data, conn, curs)

                if lobby is not None:
                    lobbymessages = len(lobby) - 1
                    lobbycounter = 0
                    while lobbycounter <= lobbymessages:
                        self.outputs.append(lobby[lobbycounter])
                        lobbycounter = lobbycounter + 1
                    del lobby[:]
                else:
                    self.outputs.append([data['channel'], "Something went wrong with the lobby module that deals with this command and I was not given anything to say."])


            except curs.Error, e:

                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit(1)

            finally:

                if curs:
                    curs.close()

