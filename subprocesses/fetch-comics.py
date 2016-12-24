#!/usr/bin/env python

# Toon Bot - Fetcher Bot Subprocess
#
#  _____   U  ___ u   U  ___ u  _   _           ____     U  ___ u _____
# |_ " _|   \/"_ \/    \/"_ \/ | \ |"|       U | __")u    \/"_ \/|_ " _|
#   | |     | | | |    | | | |<|  \| |>       \|  _ \/    | | | |  | |
#  /| |\.-,_| |_| |.-,_| |_| |U| |\  |u        | |_) |.-,_| |_| | /| |\
# u |_|U \_)-\___/  \_)-\___/  |_| \_|         |____/  \_)-\___/ u |_|U
# _// \\_     \\         \\    ||   \\,-.     _|| \\_       \\   _// \\_
# (__) (__)   (__)       (__)   (_")  (_/     (__) (__)     (__) (__) (__)
#
#                                   Providing 5 minute breaks since 2016
#
# By Robert Hawdon - https://robertianhawdon.me.uk/

import sys
from argparse import ArgumentParser
import MySQLdb
import random
import time
import urllib
import urllib2
import yaml
import json
import os
import os.path
import re
from tendo import singleton
from datetime import datetime, time, timedelta
from warnings import filterwarnings

filterwarnings('ignore', category = MySQLdb.Warning)

me = singleton.SingleInstance()

# To-Do, database this
defaultmode = 1

script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))
comics_dirpath = script_dirpath + '/../comics'

# sys.path.insert(0, comics_dirpath)

class FetcherBot(object):
    def __init__(self, config):
        # set the config object
        self.config = config

        # set mysql details
        self.mysqlserver = config.get('MYSQL_SERVER')
        self.mysqluser = config.get('MYSQL_USER')
        self.mysqlpass = config.get('MYSQL_PASS')
        self.mysqldb = config.get('MYSQL_DB')

        try:
            conn = MySQLdb.Connection(self.mysqlserver, self.mysqluser, self.mysqlpass, self.mysqldb)
            curs = conn.cursor()
            conn.set_character_set('utf8')
            curs.execute('SET NAMES utf8;')
            curs.execute('SET CHARACTER SET utf8;')
            curs.execute('SET character_set_connection=utf8;')
            cmd = "SELECT value FROM tbl_system WHERE name = 'fetch_timeout'"
            curs.execute(cmd)
            result = curs.fetchall()
            for timeout in result:
                default_timeout = timeout[0]

        except curs.Error, e:
            print "Error 1 %d: %s" % (e.args[0], e.args[1])
            sys.exit(1)

        packs = [None]

        for directory in os.listdir(comics_dirpath):
            if os.path.isdir(comics_dirpath + "/" + directory):
                packs.append(directory)

        for packdirectory in packs:
            if packdirectory is None:
                comicpath = comics_dirpath
                packconfig = False
            else:
                comicpath = comics_dirpath + "/" + packdirectory
                if os.path.isfile(comicpath + "/toonpack.yml"):
                    packconfig = True
                    packconfigdata = yaml.load(open(comicpath + "/toonpack.yml"))
                    packuuid = packconfigdata["PackUUID"]
                    packcode = packconfigdata["PackCode"]
                    packname = packconfigdata["PackName"]
                    packdesc = packconfigdata["PackDescription"]
                    packversion = packconfigdata["Version"]
                    packgen = packconfigdata["PackGen"]
                    packprefs = packconfigdata["CustomPreferences"]
                    print packprefs
                    cmd = "SELECT ID, UUID, packcode, packname, packdesc, version, packgen, directory FROM tbl_packs WHERE UUID = %s"
                    curs.execute(cmd, ([packuuid]))
                    result = curs.fetchall()
                    if len(result) == 0:
                        cmd = "INSERT INTO tbl_packs (UUID, packcode, packname, packdesc, version, packgen) VALUES (%s, %s, %s, %s, %s, %s)"
                        curs.execute(cmd, ([packuuid], [packcode], [packname], [packdesc], [packversion], [packgen]))
                        packid = conn.insert_id()
                        conn.commit()
                    else:
                        for packdetails in result:
                            packid = packdetails[0]
                            dbpackuuid = packdetails[1]
                            dbpackcode = packdetails[2]
                            dbpackname = packdetails[3]
                            dbpackdesc = packdetails[4]
                            dbpackversion = packdetails[5]
                            dbpackgen = packdetails[6]
                            dbdirectory = packdetails[7]
                            if dbpackcode != packcode or dbpackname != packname or dbpackdesc != packdesc or dbpackversion != packversion or dbpackgen != packgen or dbdirectory != packdirectory:
                                cmd = "UPDATE tbl_packs SET packcode = %s, packname = %s, packdesc = %s, version = %s, packgen = %s, directory = %s WHERE UUID = %s"
                                curs.execute(cmd, ([packcode], [packname], [packdesc], [packversion], [packgen], [packdirectory], [packuuid]))
                                conn.commit()
                else:
                    packconfig = False

            for file in os.listdir(comicpath):
                if packconfig is False:
                    packid = None
                if file.endswith(".py"):
                    modulename = re.sub(r'.py$', '', file)
                    sys.path.insert(0, comicpath)
                    sys.modules['comicmodule'] = __import__(modulename)
                    comicnamecode = modulename
                    cmd = "SELECT fetch_timeout, mode FROM tbl_comics WHERE comicname = %s"
                    curs.execute(cmd, ([comicnamecode]))
                    result = curs.fetchall()
                    if len(result) == 0:
                        timeout = int(default_timeout)
                        mode = 255
                    else:
                        for timeout in result:
                            comic_timeout = timeout[0]
                            mode = timeout[1]
                            if comic_timeout is not None:
                                timeout = comic_timeout
                            else:
                                timeout = int(default_timeout)
                    from comicmodule import fetch_comic
                    if mode == 0 or mode == 3:
                        status, comichash, title, comic, text, link, comicname, comictitle = fetch_comic(comicnamecode, timeout)
                    elif mode == 255:
                        status, comichash, title, comic, text, link, comicname, comictitle = (True, None, None, None, None, None, comicnamecode, comicnamecode)
                    else:
                        status = False
                    del sys.modules['comicmodule']

                    if status is True:
                        currenttime = datetime.utcnow()
                        try:
                            cmd = "SELECT comicname, displayname, pack FROM tbl_comics WHERE comicname = %s"
                            curs.execute(cmd, ([comicname]))
                            result = curs.fetchall()
                            if len(result) == 0:
                                cmd = "INSERT INTO tbl_comics (comicname, displayname, pack, mode) VALUES (%s, %s, %s, %s)"
                                curs.execute(cmd, ([comicname], [comictitle], [packid], [defaultmode]))
                                conn.commit()
                                dbcomicmode = 0
                            else:
                                for comiclist in result:
                                    dbcomicname = comiclist[0]
                                    dbdisplayname = comiclist[1]
                                    dbpackid = comiclist[2]
                                if dbdisplayname != comictitle:
                                    cmd = "UPDATE tbl_comics SET displayname = %s WHERE comicname = %s"
                                    curs.execute(cmd, ([comictitle], [comicname]))
                                    conn.commit()
                                if dbpackid != packid:
                                    cmd = "UPDATE tbl_comics SET pack = %s WHERE comicname = %s"
                                    curs.execute(cmd, ([packid], [comicname]))
                                    conn.commit()

                        except curs.Error, e:
                            print "Error 1 %d: %s" % (e.args[0], e.args[1])
                            pass

                        try:
                            cmd = "SELECT D.comichash FROM tbl_comic_data D JOIN tbl_comics C ON C.latest = D.comichash WHERE D.comichash = %s"
                            curs.execute(cmd, ([comichash]))
                            result = curs.fetchall()
                            if len(result) == 0:
                                cmd = "INSERT IGNORE INTO tbl_comic_data (comichash, title, image, text, pageurl, fetchtime) VALUES (%s, %s, %s, %s, %s, %s)"
                                curs.execute(cmd, ([comichash], [title], [comic], [text], [link], [currenttime]))
                                cmd = "UPDATE tbl_comics SET latest = %s, lastfetched = %s WHERE comicname = %s"
                                curs.execute(cmd, ([comichash], [currenttime], [comicname]))
                                conn.commit()

                        except curs.Error, e:
                            print "Error %d: %s" % (e.args[0], e.args[1])
                            pass

        if curs:
            curs.close()

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Full path to config file.',
        metavar='path'
    )
    return parser.parse_args()

# load args with config path
args = parse_args()
config = yaml.load(open(args.config or script_dirpath + '/../toonbot.conf', 'r'))
FetcherBot(config)
