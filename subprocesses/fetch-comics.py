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

me = singleton.SingleInstance()

script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))
comics_dirpath = script_dirpath + '/../comics'

sys.path.insert(0, comics_dirpath)

class FetcherBot(object):
    def __init__(self, config):
        # set the config object
        self.config = config

        # set mysql details
        self.mysqlserver = config.get('MYSQL_SERVER')
        self.mysqluser = config.get('MYSQL_USER')
        self.mysqlpass = config.get('MYSQL_PASS')
        self.mysqldb = config.get('MYSQL_DB')

        for file in os.listdir(comics_dirpath):
            if file.endswith(".py"):
                modulename = re.sub(r'.py$', '', file)
                sys.modules['comicmodule'] = __import__(modulename)
                from comicmodule import fetch_comic
                status, comichash, title, comic, text, link, comicname, comictitle = fetch_comic()
                del sys.modules['comicmodule']

                if status is True:
                    try:
                        conn = MySQLdb.Connection(self.mysqlserver, self.mysqluser, self.mysqlpass, self.mysqldb)
                        curs = conn.cursor()
                        conn.set_character_set('utf8')
                        curs.execute('SET NAMES utf8;')
                        curs.execute('SET CHARACTER SET utf8;')
                        curs.execute('SET character_set_connection=utf8;')
                        cmd = "SELECT comicname, displayname FROM tbl_comics WHERE comicname = %s"
                        curs.execute(cmd, ([comicname]))
                        result = curs.fetchall()
                        if len(result) == 0:
                            cmd = "INSERT INTO tbl_comics (comicname, displayname) VALUES (%s, %s)"
                            curs.execute(cmd, ([comicname], [comictitle]))
                            conn.commit()
                        else:
                            for comic in result:
                                dbcomicname = comic[0]
                                dbdisplayname = comic[1]
                            if dbdisplayname != comictitle:
                                cmd = "UPDATE tbl_comics SET displayname = %s WHERE comicname = %s"
                                curs.execute(cmd, ([comictitle], [comicname]))
                                conn.commit()

                    except curs.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)

                    try:
                        cmd = "SELECT comichash FROM tbl_comic_data WHERE comichash = %s"
                        curs.execute(cmd, ([comichash]))
                        result = curs.fetchall()
                        if len(result) == 0:
                            cmd = "INSERT INTO tbl_comic_data (comichash, title, image, text, pageurl) VALUES (%s, %s, %s, %s, %s)"
                            curs.execute(cmd, ([comichash], [title], [comic], [text], [link]))
                            cmd = "UPDATE tbl_comics SET latest = %s WHERE comicname = %s"
                            curs.execute(cmd, ([comichash], [comicname]))
                            conn.commit()

                    except curs.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)

                    finally:
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
config = yaml.load(open(args.config or script_dirpath + '/../../../rtmbot.conf', 'r'))
FetcherBot(config)
