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

def feedback(data, conn, curs):
    try:
        feedbackmessage = data['text'].split(' ', 1)[1]
        cmd = "INSERT INTO tbl_feedback (slackuser, message) VALUES (%s, %s);"
        curs.execute(cmd, ([data['user']], [feedbackmessage]))
        conn.commit()
        outputs.append([data['channel'], "Thanks for the feedback."])
    except Exception, e:
        outputs.append([data['channel'], "Please type `feedback` followed by your message."])
    return outputs
