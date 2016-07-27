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
