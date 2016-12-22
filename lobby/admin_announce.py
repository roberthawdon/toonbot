#!/usr/bin/env python
from __main__ import *
import time
import MySQLdb
import sys
import json
import urllib2
import re
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
    return outputs
