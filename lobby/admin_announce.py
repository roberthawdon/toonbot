#!/usr/bin/env python
from __main__ import *
import time
import MySQLdb
import sys
import json
import urllib2
import re

outputs = []

slacktoken = config["SLACK_TOKEN"]
botuser = config["BOT_USER"]

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
