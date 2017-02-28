from __main__ import *
import json
import urllib2
from confload import ToonbotConf

config = ToonbotConf()

slacktoken = config["SLACK_TOKEN"]


def getbotuser():
    req = "https://slack.com/api/auth.test?token=" + slacktoken
    response = urllib2.urlopen(req)
    jsonres = json.load(response)
    botuser = jsonres["user_id"]
    return botuser
