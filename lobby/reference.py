#!/usr/bin/env python
from __main__ import *
import time
import MySQLdb
import sys
import re
from datetime import datetime
import os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from confload import ToonbotConf

config = ToonbotConf()

outputs = []

slacktoken = config["SLACK_TOKEN"]

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

def help(data):
    outputs.append([data['channel'], "Type `list` to view a list of available comics. You can subscribe to a comic by sending its name. Once subscribed, you'll receive the latest comic in a few minutes. If you change your mind, you can also unsubscribe by sending its name again. The `list` command will be updated to reflect which comics you are currently subscribed to.\nI should not be added to public or private chat rooms, but in the event I am, I will not talk. I've been designed to only talk in direct messages.\nI have been programmed to only post comics during working hours. If you'd like to change this, type `start HH:MM:SS` and `end HH:MM:SS` to adjust when I send comics to you.\nTo change the colour of the message sections you can use the `postcolour` and `posttextcolour` commands followed by a Hex colour code such as `#d3f6aa`.\nTo reset your preferences to the defaults, type `clear preferences` or clear spesific preferences by repacing the argument with `reset`.\nTo see your current preferences, say `show preferences`."])
    return outputs

def about(data):
    outputs.append([data['channel'], "*Toonbot*\n_Providing 5 minute breaks since 2016_\nWritten by Robert Hawdon\nhttps://github.com/roberthawdon/toonbot"])
    return outputs

def showversion(data, curs, botversion, botcodename):
    cmd = "SELECT value FROM tbl_system WHERE name = 'db_version'"
    curs.execute(cmd)
    result = curs.fetchall()
    for verinfo in result:
        dbversion = verinfo[0]
    cmd = "SELECT value FROM tbl_system WHERE name = 'db_latest_migration'"
    curs.execute(cmd)
    result = curs.fetchall()
    for verinfo in result:
        dbrevisionraw = verinfo[0]
    dbrevision = re.sub('\.sql$', '', dbrevisionraw)
    dbrevisiondate = datetime.strptime(dbrevision, "%Y%m%d%H%M%S")
    outputs.append([data['channel'], "Toonbot Version: " + botversion + " (" + botcodename + ")\nDatabase Version: " + dbversion + "\nDatabase Revision: " + dbrevisiondate.strftime('%a %d %b %Y at %H:%M:%S') + ""])
    return outputs
