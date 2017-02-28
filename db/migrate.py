#!/usr/bin/env python

import time
import MySQLdb
import sys
import os
import yaml
import re
from prettytable import PrettyTable
from argparse import ArgumentParser
from warnings import filterwarnings


filterwarnings('ignore', category = MySQLdb.Warning)

print "Toon Bot data migration V1.4"
print "----------------------------"

def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-c',
        '--config',
        help='Full path to config file.',
        metavar='path'
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    directory = os.path.dirname(sys.argv[0])
    if not directory.startswith('/'):
        directory = os.path.abspath("{}/{}".format(os.getcwd(),
                                directory
                                ))

    config = yaml.load(file(args.config or '../toonbot.conf', 'r'))
    mysqlserver = config["MYSQL_SERVER"]
    mysqluser = config["MYSQL_USER"]
    mysqlpass = config["MYSQL_PASS"]
    mysqldb = config["MYSQL_DB"]

print "\nStarting migration...\n"

for file in sorted(os.listdir("migrations")):
    if file.endswith(".sql"):
        try:
            conn = MySQLdb.Connection(mysqlserver, mysqluser, mysqlpass, mysqldb)
            curs = conn.cursor()
            cmd = "SELECT migration FROM tbl_migrations WHERE migration = %s AND run = 1"
            curs.execute(cmd, ([file]))
            result = curs.fetchall()
            if len(result) == 0:
                cmd = "INSERT IGNORE INTO tbl_migrations SET migration = %s"
                curs.execute(cmd, ([file]))
                conn.commit()
                ignorestatement = False
                statement = ""
                for line in open("migrations/" + file):
                    if line.startswith('DELIMITER'):
                        if not ignorestatement:
                            ignorestatement = True
                            continue
                        else:
                            ignorestatement = False
                            line = " ;"
                    if re.match(r'--', line):  # ignore sql comment lines
                        continue
                    if not re.search(r'[^-;]+;', line) or ignorestatement:  # keep appending lines that don't end in ';' or DELIMITER has been called
                        statement = statement + line
                    else:  # when you get a line ending in ';' then exec statement and reset for next statement
                        statement = statement + line
                        #print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
                        try:
                            #print statement
                            curs.execute(statement)
                            conn.commit()
                            statement = ""
                        except curs.Error, e:
                            print(file + " - Error applying (" + str(e) + ")\nTerminating.")
                            sys.exit(1)
                cmd = "UPDATE tbl_migrations SET run = 1 WHERE migration = %s"
                curs.execute(cmd, ([file]))
                conn.commit()
                cmd = "UPDATE tbl_system SET value = %s WHERE name = \"db_latest_migration\""
                curs.execute(cmd, ([file]))
                conn.commit()
                print(file + " - Applied")
            else:
                print(file + " - Skipping - Already applied")
        except curs.Error, e:
            print str(e)
