from __main__ import *
import time
import json
import urllib2
import MySQLdb
from datetime import datetime
from checktime import runat
from checkaccount import checkaccount

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

def checkruntime():
    try:
        conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
        curs = conn.cursor()
        conn.set_character_set('utf8')
        curs.execute('SET NAMES utf8;')
        curs.execute('SET CHARACTER SET utf8;')
        curs.execute('SET character_set_connection=utf8;')
        cmd = "SELECT value FROM tbl_system WHERE name = 'janitor_run'"
        curs.execute(cmd)
        result = curs.fetchall()
        for preference in result:
            scheduled = preference[0]

        return scheduled

    except curs.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    # scheduled = "02:05:30" # May be reimplemented for if the database entry is unavailable.

cron = 60

crontable = []
crontable.append([cron, "janitor"])
outputs = []

def janitor():
    scheduled = checkruntime()
    if runat(scheduled, cron):
        checkaccount()
