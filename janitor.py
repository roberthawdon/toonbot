from __main__ import *
import time
import json
import urllib2
import MySQLdb
from datetime import datetime
from checktime import runat
from checktimezone import checktimezone

scheduled = "02:05:30"
cron = 60

crontable = []
crontable.append([cron, "janitor"])
outputs = []

def janitor():
    if runat(scheduled, cron):
        checktimezone()