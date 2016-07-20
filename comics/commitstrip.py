#!/usr/bin/env python
import time
import hashlib
import random
import socket
import urllib2
import feedparser
import re
from BeautifulSoup import BeautifulSoup
from datetime import datetime, time, timedelta

def fetch_comic(comicname, fetch_timeout):
    comictitle = "CommitStrip"

    try:
        url = 'http://www.commitstrip.com/en/feed/'
        headers = { 'User-Agent' : 'Toonbot/1.0' }
        req = urllib2.Request(url, None, headers)
        site = urllib2.urlopen(req, timeout=fetch_timeout).read()
        feed = feedparser.parse(site)
        result = feed.entries[0].content[0]
        soup = BeautifulSoup(result['value'])
        comic = (soup.find("img", attrs={"class":re.compile("^alignnone size-full wp-image-")})["src"]).encode('utf8')
        title = feed.entries[0].title.encode('utf8')
        link = feed.entries[0].link.encode('utf8')
        prehash = comic
        hash = hashlib.md5()
        hash.update(prehash)
        comichash = hash.hexdigest()
        text = None
        return (True, comichash, title, comic, text, link, comicname, comictitle)

    except Exception, e:
        return (False, None, None, None, None, None, comicname, comictitle)
