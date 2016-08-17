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

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

def comicstatus(data, curs):
    tablecomics = PrettyTable(["Comic", "Subscribers", "Last Updated", "Status"])
    tablecomics.align["Comic"] = "l"
    tablecomics.padding_width = 1
    cmd = "SELECT C.comicname, C.lastfetched, C.mode, COUNT(S.comicname) FROM tbl_comics C LEFT JOIN tbl_subscriptions S ON C.comicname = S.comicname GROUP BY C.comicname ORDER BY C.comicname"
    curs.execute(cmd)
    result = curs.fetchall()
    for comics in result:
        if comics[2] == 1:
            modeflag = "Disabled and Hidden"
        elif comics[2] == 2:
            modeflag = "Disabled"
        elif comics[2] == 3:
            modeflag = "Hidden (Secret)"
        else:
            modeflag = ""
        now = datetime.utcnow()
        if comics[1] is not None:
            lastfetched = dayssince(now, comics[1])
        else:
            lastfetched = "Never"
        tablecomics.add_row([comics[0], comics[3], lastfetched, modeflag])
    outputs.append([data['channel'], "```" + str(tablecomics) + "```"])
    return outputs


