#!/usr/bin/env python
from __main__ import *
import time
import MySQLdb
import sys
import json
import urllib2
import re
from prettytable import PrettyTable
from datetime import datetime, time, timedelta

import os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from checktime import dayssince

outputs = []

slacktoken = config["SLACK_TOKEN"]

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

def list(data, curs):
    tablecomics = PrettyTable(["Comic", "Subscribed", "Last Updated"])
    tablecomics.align["Comic"] = "l"
    tablecomics.padding_width = 1
    cmd = "SELECT C.comicname, S.slackuser, C.lastfetched FROM tbl_comics C LEFT JOIN tbl_subscriptions S ON S.comicname = C.comicname AND S.slackuser = %s WHERE C.mode = 0"
    curs.execute(cmd, ([data['user']]))
    result = curs.fetchall()
    for comics in result:
        if comics[1] == data['user']:
            enabledflag = "Yes"
        else:
            enabledflag = ""
        now = datetime.utcnow()
        if comics[2] is not None:
            lastfetched = dayssince(now, comics[2])
        else:
            lastfetched = "Never"
        tablecomics.add_row([comics[0], enabledflag, lastfetched])
    outputs.append([data['channel'], "Here is a list of available comics:\n```" + str(tablecomics) + "```\nType the name of each comic you want to subscribe to as an individual message. Type the name again to unsubscribe."])
    return outputs

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
    return outputs
