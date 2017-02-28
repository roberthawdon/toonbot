from __main__ import *
import shutil
import tempfile
import MySQLdb
import sys
import json
import requests
import urllib2
import glob
import re
import zipfile
import yaml
from confload import ToonbotConf

import os, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

comics_dirpath = currentdir + "/comics"

# To-Do, database this
defaultmode = 1

config = ToonbotConf()

slacktoken = config["SLACK_TOKEN"]

mysqlserver = config["MYSQL_SERVER"]
mysqluser = config["MYSQL_USER"]
mysqlpass = config["MYSQL_PASS"]
mysqldb = config["MYSQL_DB"]

def autoupdatepacks():
    try:
        tbpackid = []
        tbpackuuid = []
        tbpackcode = []
        tbpackname = []
        tbgitpack = []
        tbpackversion = []
        conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
        curs = conn.cursor()
        cmd = "SELECT ID, UUID, packcode, packname, github, version FROM tbl_packs WHERE autoupdate = 1"
        curs.execute(cmd)
        result = curs.fetchall()
        for pack in result:
            tbpackid.append(pack[0])
            tbpackuuid.append(pack[1])
            tbpackcode.append(pack[2])
            tbpackname.append(pack[3])
            tbgitpack.append(pack[4])
            tbpackversion.append(pack[5])
        for ids in tbpackid:
            packidx = tbpackid.index(ids)
            gitapiurl = "https://api.github.com/repos/" + tbgitpack[packidx] + "/releases/latest"

            response = urllib2.urlopen(gitapiurl)
            jsonres = json.load(response)
            packlatest = jsonres["tag_name"]
            packlocation = jsonres["zipball_url"]
            if float(tbpackversion[packidx]) < float(packlatest):
                tmppackdir = tempfile.mkdtemp()
                response = requests.get(packlocation, stream=True, allow_redirects=True)
                with open(tmppackdir + "/pack.zip", 'wb') as out_file:
                    shutil.copyfileobj(response.raw, out_file)
                del response
                zip_ref = zipfile.ZipFile(tmppackdir + "/pack.zip", 'r')
                zip_ref.extractall(tmppackdir)
                zip_ref.close()
                tmpname = tbgitpack[packidx].replace("/", "-")
                tmpdir = glob.glob(tmppackdir + "/" + tmpname + "*")

                packconfigdata = yaml.load(open(tmpdir[0] + "/toonpack.yml"))
                packuuid = packconfigdata["PackUUID"]
                packcode = packconfigdata["PackCode"]
                packname = packconfigdata["PackName"]
                packdesc = packconfigdata["PackDescription"]
                packversion = packconfigdata["Version"]
                packgen = packconfigdata["PackGen"]
                packprefs = packconfigdata["CustomPreferences"]
                for key, value in packprefs.iteritems():
                    cmd = "INSERT IGNORE INTO tbl_custom_preferences (`name`, `default`, `description`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `default` = %s, `description` = %s"
                    curs.execute(cmd, ([key], [value["default"]], [value["description"]], [value["default"]], [value["description"]]))
                    conn.commit()

                cmd = "UPDATE tbl_packs SET packcode = %s, packname = %s, packdesc = %s, version = %s, packgen = %s, directory = %s WHERE UUID = %s"
                curs.execute(cmd, ([packcode], [packname], [packdesc], [packversion], [packgen], [packcode], [packuuid]))
                conn.commit()
                packdirectory = comics_dirpath + "/" + packcode
                shutil.rmtree(packdirectory)
                shutil.move(tmpdir[0], packdirectory)
                shutil.rmtree(tmppackdir)
                for file in os.listdir(packdirectory):
                    if file.endswith(".py"):
                        modulename = re.sub(r'.py$', '', file)
                        comicnamecode = modulename
                        comicname, comictitle = (comicnamecode, comicnamecode)
                        cmd = "INSERT IGNORE INTO tbl_comics (comicname, displayname, pack, mode) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE comicname = %s, displayname = %s, pack = %s"
                        curs.execute(cmd, ([comicname], [comictitle], [tbpackid[packidx]], [defaultmode], [comicname], [comictitle], [tbpackid]))
                        conn.commit()

    except urllib2.HTTPError, e:
        shutil.rmtree(tmppackdir)

    except IOError, e:
        shutil.rmtree(tmppackdir)
