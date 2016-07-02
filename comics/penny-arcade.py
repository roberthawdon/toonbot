#!/usr/bin/env python
import hashlib
import random
import urllib2
from BeautifulSoup import BeautifulSoup

def fetch_comic():
    comictitle = "Penny Arcade"
    comicname = "penny-arcade"

    try:
        url = 'https://www.penny-arcade.com/comic/'
        headers = { 'User-Agent' : 'Toonbot/1.0' }
        req = urllib2.Request(url, None, headers)
        site = urllib2.urlopen(req, timeout=10).read()
        soup = BeautifulSoup(site)
        div = (soup.find("div", attrs={'id':'comicFrame'}))
        title = div.find("img")["alt"]
        comic = div.find("img")["src"]
        link = (soup.find("meta", attrs={'property':'og:url'})["content"])
        prehash = comic
        hash = hashlib.md5()
        hash.update(prehash)
        comichash = hash.hexdigest()
        text = None
        return (True, comichash, title, comic, text, link, comicname, comictitle)

    except Exception, e:
        return (False, None, None, None, None, None, comicname, comictitle)
