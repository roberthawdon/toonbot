from __main__ import *
import time
import json
import urllib2
import MySQLdb
from datetime import datetime

slacktoken = config["SLACK_TOKEN"]

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

def checktimezone(userid=None):
    req = "https://slack.com/api/users.list?token=" + slacktoken
    response = urllib2.urlopen(req)
    jsonres = json.load(response)
    slackuser = []
    tzoffset = []
    for userlist in jsonres["members"]:
        slackuser.append(userlist["id"])
        if 'tz_offset' in userlist:
            tzoffset.append(userlist["tz_offset"])
        else:
            tzoffset.append(None)
    try:
        conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
        curs = conn.cursor()
        if userid is None:
                cmd = "SELECT slackuser, tzoffset FROM tbl_users"
                curs.execute(cmd)
                result = curs.fetchall()
                tbslackusers = []
                tbtzoffset = []
                for toonusers in result:
                    tbslackusers.append(toonusers[0])
                    tbtzoffset.append(toonusers[1])
                for user in tbslackusers:
                    tbuseridx = tbslackusers.index(user)
                    useridx = slackuser.index(user)
                    if tbtzoffset[tbuseridx] != tzoffset[useridx]:
                        try:
                            cmd = "UPDATE tbl_users SET tzoffset = %s WHERE slackuser = %s"
                            curs.execute(cmd, (tzoffset[useridx], user))
                            result = curs.fetchall()
                            conn.commit()
                        except curs.Error, e:

                            print "Error %d: %s" % (e.args[0], e.args[1])
                            sys.exit(1)

        else:
            useridx = slackuser.index(userid)
            cmd = "UPDATE tbl_users SET tzoffset = %s WHERE slackuser = %s"
            curs.execute(cmd, (tzoffset[useridx], userid))
            result = curs.fetchall()
            conn.commit()
            
    except curs.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
