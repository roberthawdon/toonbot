#!/usr/bin/env python
from __main__ import *
import time
import MySQLdb
import sys
import json
import urllib2
import re
from prettytable import PrettyTable
from confload import ToonbotConf

config = ToonbotConf()

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
            cmd = "INSERT IGNORE INTO tbl_preferences (userID, name, value) (SELECT ID, 'daystart', %s FROM tbl_users WHERE slackuser = %s) ON DUPLICATE KEY UPDATE value = %s"
            curs.execute(cmd, ([timesetting], [data['user']], [timesetting]))
            conn.commit()
            outputs.append([data['channel'], "OK, I won't post any comics until `" + timesetting + "`. If you find comics are being sent to you at incorrect times, ensure your timezone is correct on Slack."])
        elif timesetting == 'reset':
            cmd = "DELETE FROM tbl_preferences WHERE userID = (SELECT ID FROM tbl_users WHERE slackuser = %s) AND name = 'daystart'"
            curs.execute(cmd, ([data['user']]))
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
            cmd = "INSERT IGNORE INTO tbl_preferences (userID, name, value) (SELECT ID, 'dayend', %s FROM tbl_users WHERE slackuser = %s) ON DUPLICATE KEY UPDATE value = %s"
            curs.execute(cmd, ([timesetting], [data['user']], [timesetting]))
            conn.commit()
            outputs.append([data['channel'], "OK, I won't post any comics after `" + timesetting + "`. If you find comics are being sent to you at incorrect times, ensure your timezone is correct on Slack."])
        elif timesetting == 'reset':
            cmd = "DELETE FROM tbl_preferences WHERE userID = (SELECT ID FROM tbl_users WHERE slackuser = %s) AND name = 'dayend'"
            curs.execute(cmd, ([data['user']]))
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
            cmd = "INSERT IGNORE INTO tbl_preferences (userID, name, value) (SELECT ID, 'postcolor', %s FROM tbl_users WHERE slackuser = %s) ON DUPLICATE KEY UPDATE value = %s"
            curs.execute(cmd, ([hex_code], [data['user']], [hex_code]))
            conn.commit()
            outputs.append([data['channel'], "OK, I can do that for you."])
        elif coloursetting == 'reset':
            cmd = "DELETE FROM tbl_preferences WHERE userID = (SELECT ID FROM tbl_users WHERE slackuser = %s) AND name = 'postcolor'"
            curs.execute(cmd, ([data['user']]))
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
            cmd = "INSERT IGNORE INTO tbl_preferences (userID, name, value) (SELECT ID, 'posttextcolor', %s FROM tbl_users WHERE slackuser = %s) ON DUPLICATE KEY UPDATE value = %s"
            curs.execute(cmd, ([hex_code], [data['user']], [hex_code]))
            conn.commit()
            outputs.append([data['channel'], "OK, I can do that for you."])
        elif coloursetting == 'reset':
            cmd = "DELETE FROM tbl_preferences WHERE userID = (SELECT ID FROM tbl_users WHERE slackuser = %s) AND name = 'posttextcolor'"
            curs.execute(cmd, ([data['user']]))
            conn.commit()
            outputs.append([data['channel'], "Your colour setting has been reset."])
        else:
            outputs.append([data['channel'], "Sorry, I can't quite figure out what that colour is. Please pass it to me in a hex format, or `reset` to use the default."])
    except Exception, e:
        outputs.append([data['channel'], "Please tell me a colour in a hex format or `reset` to the default."])
    return outputs

def resetprefs(data, conn, curs):
    cmd = "DELETE FROM tbl_preferences WHERE userID = (SELECT ID FROM tbl_users WHERE slackuser = %s)"
    curs.execute(cmd, ([data['user']]))
    conn.commit()
    outputs.append([data['channel'], "Your preferences have been reset. Your subscriptions are unaffected."])
    return outputs

def showprefs(data, conn, curs):
    cmd = "SELECT ID FROM tbl_users WHERE slackuser = %s"
    curs.execute(cmd, [data['user']])
    result = curs.fetchall()
    for users in result:
        userid = users[0]
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
    cmd = "SELECT name, value FROM tbl_preferences WHERE userID = %s"
    curs.execute(cmd, [userid])
    result = curs.fetchall()
    prefname = []
    prefvalue = []
    for preferences in result:
        prefname.append(preferences[0])
        prefvalue.append(preferences[1])
    if 'daystart' in prefname:
        daystartmessage = "You have requested comics won't be posted before `" + prefvalue[prefname.index("daystart")] + "`."
    else:
        daystartmessage = "Your comics won't be posted before `" + defaultstarttime + "`. This is the time set by your administrator, you can override this using the `start` command."
    if 'dayend' in prefname:
        dayendmessage = "You have requested comics won't be posted after `" + prefvalue[prefname.index("dayend")] + "`."
    else:
        dayendmessage = "Your comics won't be posted after `" + defaultendtime + "`. This is the time set by your administrator, you can override this using the `end` command."
    if 'postcolor' in prefname:
        postcolormessage = "You have chosen this colour (#" + prefvalue[prefname.index("postcolor")] + ") to accompany the comic images."
    else:
        postcolormessage = "This colour (#" + defaultpostcolor + ") will accompany the comic images. This is the default value and can be changed with the `postcolour` command."
    if 'posttextcolor' in prefname:
        posttextcolormessage = "You have chosen this colour (#" + prefvalue[prefname.index("posttextcolor")] + ") to be used with the text field used by some comics."
    else:
        posttextcolormessage = "This colour (#" + defaultposttextcolor + ") will be used with the text field used by certain comics. This is the default value and can be changed with the `posttextcolour` command."
    outputs.append([data['channel'], daystartmessage + "\n" + dayendmessage + "\n" + postcolormessage + "\n" + posttextcolormessage])
    return outputs
