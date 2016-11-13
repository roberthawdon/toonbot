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

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

def globalstarttime(data, conn, curs):
    try:
        timesetting = data['text'].split(' ', 1)[1]
        if re.match(r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$', timesetting):
            cmd = "UPDATE tbl_system SET value = %s WHERE name = 'tb_daystart'"
            curs.execute(cmd, ([timesetting]))
            conn.commit()
            outputs.append([data['channel'], "Global day start has been set to `" + timesetting + "` unless overridden by users."])
        else:
            outputs.append([data['channel'], "Please specify the time in the `HH:MM:SS` format."])
    except Exception, e:
        outputs.append([data['channel'], "Please specify a time in the `HH:MM:SS` format."])
    return outputs

def globalendtime(data, conn, curs):
    try:
        timesetting = data['text'].split(' ', 1)[1]
        if re.match(r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$', timesetting):
            cmd = "UPDATE tbl_system SET value = %s WHERE name = 'tb_dayend'"
            curs.execute(cmd, ([timesetting]))
            conn.commit()
            outputs.append([data['channel'], "Global day end has been set to `" + timesetting + "` unless overridden by users."])
        else:
            outputs.append([data['channel'], "Please specify the time in the `HH:MM:SS` format."])
    except Exception, e:
        outputs.append([data['channel'], "Please specify a time in the `HH:MM:SS` format."])
    return outputs

def globalpostcolor(data, conn, curs):
    try:
        coloursetting = data['text'].split(' ', 1)[1]
        if re.match(r'^#?0?[xX]?[0-9a-fA-F]{6}$', coloursetting):
            hex_code = re.sub(r'^#?0?[xX]?', '', coloursetting)
            cmd = "UPDATE tbl_system SET value = %s WHERE name = 'postcolor'"
            curs.execute(cmd, ([hex_code]))
            conn.commit()
            outputs.append([data['channel'], "Default post colour changed."])
        else:
            outputs.append([data['channel'], "Please pass it to me in a hex format."])
    except Exception, e:
        outputs.append([data['channel'], "Please tell me a colour in a hex format."])
    return outputs

def globalposttextcolor(data, conn, curs):
    try:
        coloursetting = data['text'].split(' ', 1)[1]
        if re.match(r'^#?0?[xX]?[0-9a-fA-F]{6}$', coloursetting):
            hex_code = re.sub(r'^#?0?[xX]?', '', coloursetting)
            cmd = "UPDATE tbl_system SET value = %s WHERE name = 'posttextcolor'"
            curs.execute(cmd, ([hex_code]))
            conn.commit()
            outputs.append([data['channel'], "Default post colour changed."])
        else:
            outputs.append([data['channel'], "Please pass it to me in a hex format."])
    except Exception, e:
        outputs.append([data['channel'], "Please tell me a colour in a hex format."])
    return outputs

def comicfetchtimeout(data, conn, curs):
    try:
        timesetting = data['text'].split(' ', 1)[1]
        if re.match(r'^[0-9]*$', timesetting):
            cmd = "UPDATE tbl_system SET value = %s WHERE name = 'fetch_timeout'"
            curs.execute(cmd, ([timesetting]))
            conn.commit()
            outputs.append([data['channel'], "Default comic fetching timeout has been set to `" + timesetting + "` seconds."])
        else:
            outputs.append([data['channel'], "Please specify the number of seconds to wait for a response."])
    except Exception, e:
        outputs.append([data['channel'], "Please specify the number of seconds to wait for a response."])
    return outputs

def janitorruntime(data, conn, curs):
    try:
        timesetting = data['text'].split(' ', 1)[1]
        if re.match(r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$', timesetting):
            cmd = "UPDATE tbl_system SET value = %s WHERE name = 'janitor_run'"
            curs.execute(cmd, ([timesetting]))
            conn.commit()
            outputs.append([data['channel'], "Janitor routines set to run at `" + timesetting + "` with a 60 second tolerance."])
        else:
            outputs.append([data['channel'], "Please specify the time in the `HH:MM:SS` format."])
    except Exception, e:
        outputs.append([data['channel'], "Please specify a time in the `HH:MM:SS` format."])
    return outputs
