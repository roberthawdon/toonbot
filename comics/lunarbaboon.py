#!/usr/bin/env python
import hashlib
import random
import socket
import feedparser
from BeautifulSoup import BeautifulSoup
from datetime import datetime, time, timedelta

def fetch_comic():
    comictitle = "Lunarbaboon"
    comicname = "lunarbaboon"

    try:
        feed = feedparser.parse('http://www.lunarbaboon.com/comics/rss.xml')
        result = feed.entries[0].summary_detail
        soup = BeautifulSoup(result['value'])
        comic = (soup.find("img")["src"])
        title = feed.entries[0].title
        link = feed.entries[0].link
        prehash = comic
        hash = hashlib.md5()
        hash.update(prehash)
        comichash = hash.hexdigest()
        text = None
        return (True, comichash, title, comic, text, link, comicname, comictitle)

    except Exception, e:
        return (False, None, None, None, None, None, comicname, comictitle)
