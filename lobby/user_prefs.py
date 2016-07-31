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

def setstarttime(data, conn, curs):
    try:
        timesetting = data['text'].split(' ', 1)[1]
        if re.match(r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$', timesetting):
            cmd = "INSERT IGNORE INTO tbl_user_prefs (slackuser, daystart) VALUES (%s, %s) ON DUPLICATE KEY UPDATE daystart = %s"
            curs.execute(cmd, ([data['user']], [timesetting], [timesetting]))
            conn.commit()
            outputs.append([data['channel'], "OK, I won't post any comics until `" + timesetting + "`. If you find comics are being sent to you at incorrect times, ensure your timezone is correct on Slack."])
        elif timesetting == 'reset':
            cmd = "INSERT IGNORE INTO tbl_user_prefs (slackuser, daystart) VALUES (%s, %s) ON DUPLICATE KEY UPDATE daystart = %s"
            curs.execute(cmd, ([data['user']], [None], [None]))
            conn.commit()
            outputs.append([data['channel'], "Your time setting has been reset."])
        else:
            outputs.append([data['channel'], "Sorry, didn't quite get that. Please specify the time in the `HH:MM:SS` format or `reset` to set the start time to the default."])
    except Exception, e:
        outputs.append([data['channel'], "Please specify a time in the `HH:MM:SS` format or `reset`."])
    return outputs

def setendtime(data, conn, curs):
    try:
        timesetting = data['text'].split(' ', 1)[1]
        if re.match(r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$', timesetting):
            cmd = "INSERT IGNORE INTO tbl_user_prefs (slackuser, dayend) VALUES (%s, %s) ON DUPLICATE KEY UPDATE dayend = %s"
            curs.execute(cmd, ([data['user']], [timesetting], [timesetting]))
            conn.commit()
            outputs.append([data['channel'], "OK, I won't post any comics after `" + timesetting + "`. If you find comics are being sent to you at incorrect times, ensure your timezone is correct on Slack."])
        elif timesetting == 'reset':
            cmd = "INSERT IGNORE INTO tbl_user_prefs (slackuser, dayend) VALUES (%s, %s) ON DUPLICATE KEY UPDATE dayend = %s"
            curs.execute(cmd, ([data['user']], [None], [None]))
            conn.commit()
            outputs.append([data['channel'], "Your time setting has been reset."])
        else:
            outputs.append([data['channel'], "Sorry, didn't quite get that. Please specify the time in the `HH:MM:SS` format or `reset` to set the end time to the default."])
    except Exception, e:
        outputs.append([data['channel'], "Please specify a time in the `HH:MM:SS` format or `reset`."])
    return outputs

def setpostcolour(data, conn, curs):
    try:
        coloursetting = data['text'].split(' ', 1)[1]
        if re.match(r'^#?0?[xX]?[0-9a-fA-F]{6}$', coloursetting):
            hex_code = re.sub(r'^#?0?[xX]?', '', coloursetting)
            cmd = "INSERT IGNORE INTO tbl_user_prefs (slackuser, postcolor) VALUES (%s, %s) ON DUPLICATE KEY UPDATE postcolor = %s"
            curs.execute(cmd, ([data['user']], [hex_code], [hex_code]))
            conn.commit()
            outputs.append([data['channel'], "OK, I can do that for you."])
        elif coloursetting == 'reset':
            cmd = "INSERT IGNORE INTO tbl_user_prefs (slackuser, postcolor) VALUES (%s, %s) ON DUPLICATE KEY UPDATE postcolor = %s"
            curs.execute(cmd, ([data['user']], [None], [None]))
            conn.commit()
            outputs.append([data['channel'], "Your colour setting has been reset."])
        else:
            outputs.append([data['channel'], "Sorry, I can't quite figure out what that colour is. Please pass it to me in a hex format, or `reset` to use the default."])
    except Exception, e:
        outputs.append([data['channel'], "Please tell me a colour in a hex format or `reset` to the default."])
    return outputs

def setposttextcolour(data, conn, curs):
    try:
        coloursetting = data['text'].split(' ', 1)[1]
        if re.match(r'^#?0?[xX]?[0-9a-fA-F]{6}$', coloursetting):
            hex_code = re.sub(r'^#?0?[xX]?', '', coloursetting)
            cmd = "INSERT IGNORE INTO tbl_user_prefs (slackuser, posttextcolor) VALUES (%s, %s) ON DUPLICATE KEY UPDATE posttextcolor = %s"
            curs.execute(cmd, ([data['user']], [hex_code], [hex_code]))
            conn.commit()
            outputs.append([data['channel'], "OK, I can do that for you."])
        elif coloursetting == 'reset':
            cmd = "INSERT IGNORE INTO tbl_user_prefs (slackuser, posttextcolor) VALUES (%s, %s) ON DUPLICATE KEY UPDATE posttextcolor = %s"
            curs.execute(cmd, ([data['user']], [None], [None]))
            conn.commit()
            outputs.append([data['channel'], "Your colour setting has been reset."])
        else:
            outputs.append([data['channel'], "Sorry, I can't quite figure out what that colour is. Please pass it to me in a hex format, or `reset` to use the default."])
    except Exception, e:
        outputs.append([data['channel'], "Please tell me a colour in a hex format or `reset` to the default."])
    return outputs

def resetprefs(data, conn, curs):
    cmd = "DELETE FROM tbl_user_prefs WHERE slackuser = %s"
    curs.execute(cmd, ([data['user']]))
    conn.commit()
    outputs.append([data['channel'], "Your preferences have been reset. Your subscriptions are unaffected."])
    return outputs
