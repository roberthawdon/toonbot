#!/usr/bin/env python
from __main__ import *
import time
import MySQLdb
import sys
import json
import urllib2
import re
import os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from confload import ToonbotConf

config = ToonbotConf()

outputs = []

slacktoken = config["SLACK_TOKEN"]

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

def promoteadmin(data, conn, curs, botuser):
    try:
        promoteuser = data['text'].split(' ', 1)[1]
        req = "https://slack.com/api/users.list?token=" + slacktoken
        response = urllib2.urlopen(req)
        jsonres = json.load(response)
        slackname = []
        slackuser = []
        slackbot = []
        for members in jsonres["members"]:
            slackname.append(members["name"])
            slackuser.append(members["id"])
            slackbot.append(members["is_bot"])
        try:
            indexid = slackname.index(promoteuser)
        except Exception, e:
            outputs.append([data['channel'], "Sorry, I can't find `" + promoteuser + "` on your team."])
            indexid = None
        if indexid is not None:
            promoteuserid = slackuser[indexid]
            cmd = "SELECT slackuser, admin FROM tbl_users WHERE slackuser = %s;"
            curs.execute(cmd, ([promoteuserid]))
            result = curs.fetchall()
            if not slackbot[indexid] and promoteuserid != "USLACKBOT" and promoteuser != botuser:
                if len(result) == 0:
                    outputs.append([data['channel'], "I have yet to meet <@" + promoteuserid + ">. Get them to talk to me before promoting them to admin."])
                else:
                    for userinfo in result:
                        admin = userinfo[1]
                    if admin == 0:
                        cmd = "UPDATE tbl_users SET admin = 1 WHERE slackuser = %s;"
                        curs.execute(cmd, ([promoteuserid]))
                        conn.commit()
                        cmd = "SELECT dmid FROM tbl_users WHERE slackuser = %s;"
                        curs.execute(cmd, ([promoteuserid]))
                        result = curs.fetchall()
                        for adminuser in result:
                            promoteadmindm = adminuser[0]
                        outputs.append([data['channel'], "I have given <@" + promoteuserid + "> admin privileges."])
                        outputs.append([promoteadmindm, "You have been granted admin privileges by <@" + data['user'] + ">."])
                    else:
                        outputs.append([data['channel'], "<@" + promoteuserid + "> already has admin privileges."])
            else:
                outputs.append([data['channel'], "Sorry, I believe <@" + promoteuserid + "> to be a bot, so I will not grant this user admin privileges."])
    except Exception, e:
        #print e
        outputs.append([data['channel'], "You need to provide a user to promote to admin."])
    return outputs

def revokeadmin(data, conn, curs, botuser):
    try:
        revokeuser = data['text'].split(' ', 1)[1]
        req = "https://slack.com/api/users.list?token=" + slacktoken
        response = urllib2.urlopen(req)
        jsonres = json.load(response)
        slackname = []
        slackuser = []
        slackbot = []
        for members in jsonres["members"]:
            slackname.append(members["name"])
            slackuser.append(members["id"])
            slackbot.append(members["is_bot"])
        try:
            indexid = slackname.index(revokeuser)
        except Exception, e:
            outputs.append([data['channel'], "Sorry, I can't find `" + revokeuser + "` on your team."])
            indexid = None
        if indexid is not None:
            revokeuserid = slackuser[indexid]
            cmd = "SELECT slackuser, admin FROM tbl_users WHERE slackuser = %s;"
            curs.execute(cmd, ([revokeuserid]))
            result = curs.fetchall()
            if not slackbot[indexid] and revokeuserid != "USLACKBOT" and revokeuser != botuser:
                if len(result) == 0:
                    outputs.append([data['channel'], "I haven't met <@" + revokeuserid + ">, so they do not have admin privileges."])
                else:
                    for userinfo in result:
                        slackuser = userinfo[0]
                        admin = userinfo[1]
                    if data['user'] == revokeuserid:
                        outputs.append([data['channel'], "You cannot revoke your own admin privileges."])
                    elif admin == 1:
                        cmd = "UPDATE tbl_users SET admin = 0 WHERE slackuser = %s;"
                        curs.execute(cmd, ([revokeuserid]))
                        conn.commit()
                        cmd = "SELECT dmid FROM tbl_users WHERE slackuser = %s;"
                        curs.execute(cmd, ([revokeuserid]))
                        result = curs.fetchall()
                        for adminuser in result:
                            revokeadmindm = adminuser[0]
                        outputs.append([data['channel'], "I removed <@" + revokeuserid + ">'s admin privileges."])
                        outputs.append([revokeadmindm, "Your admin privileges have been revoked by <@" + data['user'] + ">."])
                    elif admin == 2:
                        outputs.append([data['channel'], "<@" + revokeuserid + "> is a super admin. Their permissions can't be revoked with this command."])
                    else:
                        outputs.append([data['channel'], "<@" + revokeuserid + "> is not currently an admin."])
            else:
                outputs.append([data['channel'], "Sorry, I believe <@" + revokeuserid + "> to be a bot, they can not admin privileges."])
    except Exception, e:
        # print e
        outputs.append([data['channel'], "You need to provide a user to revoke admin privileges."])
    return outputs

def promotesuperadmin(data, conn, curs, botuser):
    try:
        promoteuser = data['text'].split(' ', 1)[1]
        req = "https://slack.com/api/users.list?token=" + slacktoken
        response = urllib2.urlopen(req)
        jsonres = json.load(response)
        slackname = []
        slackuser = []
        slackbot = []
        for members in jsonres["members"]:
            slackname.append(members["name"])
            slackuser.append(members["id"])
            slackbot.append(members["is_bot"])
        try:
            indexid = slackname.index(promoteuser)
        except Exception, e:
            outputs.append([data['channel'], "Sorry, I can't find `" + promoteuser + "` on your team."])
            indexid = None
        if indexid is not None:
            promoteuserid = slackuser[indexid]
            cmd = "SELECT slackuser, admin FROM tbl_users WHERE slackuser = %s;"
            curs.execute(cmd, ([promoteuserid]))
            result = curs.fetchall()
            if not slackbot[indexid] and promoteuserid != "USLACKBOT" and promoteuser != botuser:
                if len(result) == 0:
                    outputs.append([data['channel'], "I have yet to meet <@" + promoteuserid + ">. Get them to talk to me before promoting them to super admin."])
                else:
                    for userinfo in result:
                        admin = userinfo[1]
                    if admin < 2:
                        cmd = "UPDATE tbl_users SET admin = 2 WHERE slackuser = %s;"
                        curs.execute(cmd, ([promoteuserid]))
                        conn.commit()
                        cmd = "SELECT dmid FROM tbl_users WHERE slackuser = %s;"
                        curs.execute(cmd, ([promoteuserid]))
                        result = curs.fetchall()
                        for adminuser in result:
                            promoteadmindm = adminuser[0]
                        outputs.append([data['channel'], "I have given <@" + promoteuserid + "> super admin privileges."])
                        outputs.append([promoteadmindm, "You have been granted super admin privileges by <@" + data['user'] + ">."])
                    else:
                        outputs.append([data['channel'], "<@" + promoteuserid + "> already has super admin privileges."])
            else:
                outputs.append([data['channel'], "Sorry, I believe <@" + promoteuserid + "> to be a bot, so I will not grant this user super admin privileges."])
    except Exception, e:
        #print e
        outputs.append([data['channel'], "You need to provide a user to promote to super admin."])
    return outputs

def revokesuperadmin(data, conn, curs, botuser):
    try:
        revokeuser = data['text'].split(' ', 1)[1]
        req = "https://slack.com/api/users.list?token=" + slacktoken
        response = urllib2.urlopen(req)
        jsonres = json.load(response)
        slackname = []
        slackuser = []
        slackbot = []
        for members in jsonres["members"]:
            slackname.append(members["name"])
            slackuser.append(members["id"])
            slackbot.append(members["is_bot"])
        try:
            indexid = slackname.index(revokeuser)
        except Exception, e:
            outputs.append([data['channel'], "Sorry, I can't find `" + revokeuser + "` on your team."])
            indexid = None
        if indexid is not None:
            revokeuserid = slackuser[indexid]
            cmd = "SELECT slackuser, admin FROM tbl_users WHERE slackuser = %s;"
            curs.execute(cmd, ([revokeuserid]))
            result = curs.fetchall()
            if not slackbot[indexid] and revokeuserid != "USLACKBOT" and revokeuser != botuser:
                if len(result) == 0:
                    outputs.append([data['channel'], "I haven't met <@" + revokeuserid + ">, so they do not have admin privileges."])
                else:
                    for userinfo in result:
                        slackuser = userinfo[0]
                        admin = userinfo[1]
                    if data['user'] == revokeuserid:
                        outputs.append([data['channel'], "You cannot revoke your own admin privileges."])
                    elif admin == 2:
                        cmd = "UPDATE tbl_users SET admin = 0 WHERE slackuser = %s;"
                        curs.execute(cmd, ([revokeuserid]))
                        conn.commit()
                        cmd = "SELECT dmid FROM tbl_users WHERE slackuser = %s;"
                        curs.execute(cmd, ([revokeuserid]))
                        result = curs.fetchall()
                        for adminuser in result:
                            revokeadmindm = adminuser[0]
                        outputs.append([data['channel'], "I removed <@" + revokeuserid + ">'s super admin privileges and restored them to a regular user."])
                        outputs.append([revokeadmindm, "Your admin privileges have been revoked by <@" + data['user'] + ">."])
                    else:
                        outputs.append([data['channel'], "<@" + revokeuserid + "> is not currently a super admin."])
            else:
                outputs.append([data['channel'], "Sorry, I believe <@" + revokeuserid + "> to be a bot, they can not admin privileges."])
    except Exception, e:
        # print e
        outputs.append([data['channel'], "You need to provide a user to revoke admin privileges."])
    return outputs

def claimadmin(data, conn, curs, admin):
    try:
        cmd = "SELECT slackuser, admin FROM tbl_users WHERE admin = 1 OR admin = 2;"
        curs.execute(cmd)
        result = curs.fetchall()
        if len(result) == 0:
            cmd = "UPDATE tbl_users SET admin = 1 WHERE slackuser = %s;"
            curs.execute(cmd, ([data['user']]))
            conn.commit()
            outputs.append([data['channel'], "You are now the administrator, with great power comes great responsibility."])
        elif str(admin) == "1":
            outputs.append([data['channel'], "You are already an administrator, no need to claim admin access."])
        else:
            outputs.append([data['channel'], "Nice try. "])
    except Exception, e:
        print e
    return outputs

def claimsuperadmin(data, conn, curs, admin):
    try:
        cmd = "SELECT slackuser, admin FROM tbl_users WHERE admin = 2;"
        curs.execute(cmd)
        result = curs.fetchall()
        if len(result) == 0:
            cmd = "UPDATE tbl_users SET admin = 2 WHERE slackuser = %s;"
            curs.execute(cmd, ([data['user']]))
            conn.commit()
            outputs.append([data['channel'], "You are now the super administrator."])
        elif str(admin) == "2":
            outputs.append([data['channel'], "You are already super administrator, no need to claim access again."])
        else:
            outputs.append([data['channel'], "Nice try. "])
    except Exception, e:
        print e
    return outputs
