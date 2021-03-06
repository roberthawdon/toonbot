from __main__ import *
import MySQLdb
import random
import time
import urllib2
import json
import os
import os.path
import subprocess
import sys
from checktime import workhourscheck
from rtmbot.core import Plugin, Job
from confload import ToonbotConf

config = ToonbotConf()

script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]


class QueueComicsJob(Job):
    def run(self, slack_client):
        try:
            comicname = []

            image = None
            pageurl = None
            title = None
            text = None

            conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
            curs = conn.cursor()
            conn.set_character_set('utf8')
            curs.execute('SET NAMES utf8;')
            curs.execute('SET CHARACTER SET utf8;')
            curs.execute('SET character_set_connection=utf8;')

            cmd = "SELECT name, value FROM tbl_system WHERE name = %s"
            curs.execute(cmd, ["tb_daystart"])
            result = curs.fetchall()
            for starttime in result:
                defaultstart = starttime[1]
            curs.execute(cmd, ["tb_dayend"])
            result = curs.fetchall()
            for endtime in result:
                defaultend = endtime[1]

            cmd = "SELECT comicname FROM tbl_comics WHERE (mode = 0 OR mode = 2 OR mode = 3)"
            curs.execute(cmd)
            comicresult = curs.fetchall()

            for selectedcomic in comicresult:
                comicrun = selectedcomic[0]
                cmd = "SELECT latest, displayname FROM tbl_comics WHERE comicname = %s"
                curs.execute(cmd, ([selectedcomic]))
                result = curs.fetchall()
                for comiclist in result:
                    currenthash = comiclist[0]
                    displayname = comiclist[1]

                if currenthash:
                    cmd = "SELECT U.slackuser, U.dmid, U.tzoffset, S.lastsent FROM tbl_subscriptions S LEFT OUTER JOIN tbl_users U ON U.slackuser = S.slackuser WHERE U.account_disabled = 0 AND comicname = %s"
                    curs.execute(cmd, ([comicrun]))
                    result = curs.fetchall()
                    for subscribed in result:
                        slackuser = subscribed[0]
                        offset = subscribed[2]
                        cmd = "SELECT ID FROM tbl_users WHERE slackuser = %s"
                        curs.execute(cmd, [slackuser])
                        result = curs.fetchall()
                        for users in result:
                            userid = users[0]
                        cmd = "SELECT name, value FROM tbl_preferences WHERE userID = %s"
                        curs.execute(cmd, [userid])
                        result = curs.fetchall()
                        prefname = []
                        prefvalue = []
                        for preferences in result:
                            prefname.append(preferences[0])
                            prefvalue.append(preferences[1])
                        if 'daystart' in prefname:
                            starttime = prefvalue[prefname.index("daystart")]
                        else:
                            starttime = defaultstart
                        if 'dayend' in prefname:
                            endtime = prefvalue[prefname.index("dayend")]
                        else:
                            endtime = defaultend
                        if offset is None:
                            offset = 0
                        if subscribed[3] != currenthash:
                            if workhourscheck(starttime, endtime, offset):
                                cmd = "INSERT INTO tbl_queue (slackuser, displayname, comichash) VALUES (%s, %s, %s)"
                                curs.execute(cmd, ([subscribed[0]], [displayname], [currenthash]))
                                result = curs.fetchall()
                                conn.commit()
                                cmd = "UPDATE tbl_subscriptions SET lastsent = %s WHERE slackuser = %s AND comicname = %s"
                                curs.execute(cmd, ([currenthash], [subscribed[0]], [comicrun]))
                                result = curs.fetchall()
                                conn.commit()

            subprocess.Popen(script_dirpath + '/subprocesses/post-queue.py')

        except curs.Error, e:

            print "Error %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

        finally:

            if curs:
                curs.close()
        return []

class QueueComics(Plugin):
    def register_jobs(self):
        job = QueueComicsJob(60)
        self.jobs.append(job)
