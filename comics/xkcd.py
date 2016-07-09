#!/usr/bin/env python
import time
import hashlib
import random
import urllib2
import re
from BeautifulSoup import BeautifulSoup

def fetch_comic(comicname, fetch_timeout):
    comictitle = "XKCD"

    try:
        url = 'http://xkcd.com/'
        headers = { 'User-Agent' : 'Toonbot/1.0' }
        req = urllib2.Request(url, None, headers)
        site = urllib2.urlopen(req, timeout=fetch_timeout).read()
        soup = BeautifulSoup(site)
        title = (soup.find("div", attrs={'id':'ctitle'})).next
        try:
            div = (soup.find("div", attrs={'id':'comic'}))
            comic = "http:" + (div.find("img")["src"])
            text = div.find("img")["title"]
            prehash = comic

        except Exception, e:
            comic = "http://127.0.0.1/404.png" # To Do, source an image for interactive comic purposes.
            text = "*Today's XKCD looks to be an interactive comic.*"
            prehash = url

        hash = hashlib.md5()
        hash.update(prehash)
        comichash = hash.hexdigest()
        permlinkextract = (soup.body.findAll(text=re.compile('Permanent link to this comic')))
        linktxt = re.search("(?P<url>https?://[^\s]+)", permlinkextract[0]).group("url")
        link = linktxt
        return (True, comichash, title, comic, text, link, comicname, comictitle)

    except Exception, e:
        return (False, None, None, None, None, None, comicname, comictitle)
