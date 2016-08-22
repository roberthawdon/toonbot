#!/usr/bin/env python
from __main__ import *
import time
import MySQLdb
import sys
import json
import urllib2
import re
from prettytable import PrettyTable

outputs = []

slacktoken = config["SLACK_TOKEN"]

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

def showprefs(data, conn, curs):
    cmd = "SELECT value FROM tbl_system WHERE name = 'tb_daystart'"
    curs.execute(cmd)
    result = curs.fetchall()
    for times in result:
        defaultstarttime = times[0]
    cmd = "SELECT value FROM tbl_system WHERE name = 'tb_dayend'"
    curs.execute(cmd)
    result = curs.fetchall()
    for times in result:
        defaultendtime = times[0]
    cmd = "SELECT value FROM tbl_system WHERE name = 'postcolor'"
    curs.execute(cmd)
    result = curs.fetchall()
    for color in result:
        defaultpostcolor = color[0]
    cmd = "SELECT value FROM tbl_system WHERE name = 'posttextcolor'"
    curs.execute(cmd)
    result = curs.fetchall()
    for color in result:
        defaultposttextcolor = color[0]
    cmd = "SELECT announcelevel, daystart, dayend, days, postcolor, posttextcolor FROM tbl_user_prefs WHERE slackuser = %s"
    curs.execute(cmd, ([data['user']]))
    result = curs.fetchall()
    if len(result) != 0:
        for prefs in result:
            userannouncelevel = prefs[0] # For future use
            userstarttime = prefs[1]
            if userstarttime is not None:
                starttime = userstarttime
            else:
                starttime = defaultstarttime
            userendtime = prefs[2]
            if userendtime is not None:
                endtime = userendtime
            else:
                endtime = defaultendtime
            userdays = prefs[3] # For future use
            userpostcolor = prefs[4]
            if userpostcolor is not None:
                postcolor = userpostcolor
            else:
                postcolor = defaultpostcolor
            userposttextcolor = prefs[5]
            if userposttextcolor is not None:
                posttextcolor = userposttextcolor
            else:
                posttextcolor = defaultposttextcolor
    else:
        starttime = defaultstarttime
        endtime = defaultendtime
        postcolor = defaultpostcolor
        posttextcolor = defaultposttextcolor
    outputs.append([data['channel'], "Here are your current settings:\nYour selected comics will start being posted to you at `" + starttime + "` and will stop at `" + endtime + "` local time.\nThe Hex value of the colour used for comic posts is #" + postcolor + " and any accompanying text that goes with it will use #" + posttextcolor + ".\nYou can reset any of your preferences by using `reset` as the argument, or say `clear preferences` to reset all settings to the global defaults. Your comic subscriptions will not be affected."])
    return outputs
