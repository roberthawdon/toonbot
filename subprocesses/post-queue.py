#!/usr/bin/env python

# Toon Bot - Poster Bot Subprocess
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
from tendo import singleton

me = singleton.SingleInstance()

script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))

class PosterBot(object):
    def __init__(self, config):
        # set the config object
        self.config = config

        # set slack token
        self.token = config.get('SLACK_TOKEN')

        # set mysql details
        self.mysqlserver = config.get('MYSQL_SERVER')
        self.mysqluser = config.get('MYSQL_USER')
        self.mysqlpass = config.get('MYSQL_PASS')
        self.mysqldb = config.get('MYSQL_DB')
        # self.postcolor = config.get('POST_COLOR')
        # self.posttextcolor = config.get('POST_TEXT_COLOR')

        self.process_queue()

    def process_queue(self):
        #try:
        conn = MySQLdb.Connection(self.mysqlserver, self.mysqluser, self.mysqlpass, self.mysqldb)
        curs = conn.cursor()
        conn.set_character_set('utf8')
        curs.execute('SET NAMES utf8;')
        curs.execute('SET CHARACTER SET utf8;')
        curs.execute('SET character_set_connection=utf8;')
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
        cmd = "SELECT Q.ID, Q.slackuser, Q.displayname, Q.comichash, Q.flags, U.dmid, P.postcolor, P.posttextcolor FROM tbl_queue Q LEFT JOIN tbl_users U ON U.slackuser = Q.slackuser LEFT JOIN tbl_user_prefs P ON P.slackuser = Q.slackuser WHERE Q.sent = 0"
        curs.execute(cmd)
        result = curs.fetchall()
        for items in result:
            id = items[0]
            slackuser = items[1]
            displayname = items[2]
            comichash = items[3]
            flags = items[4]
            dmid = items[5]
            userpostcolor = items[6]
            if userpostcolor is not None:
                postcolor = userpostcolor
            else:
                postcolor = defaultpostcolor
            userposttextcolor = items[7]
            if userposttextcolor is not None:
                posttextcolor = userposttextcolor
            else:
                posttextcolor = defaultposttextcolor

            cmd = "SELECT image, pageurl, title, text FROM tbl_comic_data WHERE comichash = %s"
            curs.execute(cmd, ([comichash]))
            result2 = curs.fetchall()
            for comic in result2:
                image = comic[0]
                pageurl = comic[1]
                title = comic[2]
                if title:
                    utitle = title.decode("utf-8")
                    title = utitle.encode("ascii", "ignore")
                text = comic[3]
                if text:
                    utext = text.decode("utf-8")
                    text = utext.encode("ascii", "ignore")

                if title is None:
                    title = displayname

                if text is not None:
                    body = [{"title": title,"title_link": pageurl,"author_name": displayname,"image_url": image,"color": "#" + postcolor}, {"text": text, "color": "#" + posttextcolor}]
                else:
                    body = [{"title": title,"title_link": pageurl,"author_name": displayname,"image_url": image,"color": "#" + postcolor}]

                data = body
                #print json.dumps(data)
                attachment = urllib.quote(str(json.dumps(data)))
                url = "https://slack.com/api/chat.postMessage?token=" + self.token + "&channel=" + dmid + "&attachments=" + attachment + "&as_user=true"
                req = urllib2.Request(url)
                response = urllib2.urlopen(req)
                # print response.read()
                image is None
                pageurl is None
                title is None
                text is None
                jsonres = json.load(response)
                if jsonres["ok"] is True:
                    cmd = "UPDATE tbl_queue SET sent = 1 WHERE ID = %s"
                    curs.execute(cmd, ([id]))
                    conn.commit()
                else:
                    errormessage = jsonres["error"]
                    cmd = "UPDATE tbl_queue SET flags = 1, errormessage = %s WHERE ID = %s"
                    curs.execute(cmd, ([errormessage], [id]))
                    cmd = "INSERT INTO tbl_queue_errors (errormessage, queueID) VALUES (%s, %s)"
                    curs.execute(cmd, ([errormessage], [id]))
                    conn.commit()

            time.sleep(1)

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
PosterBot(config)
