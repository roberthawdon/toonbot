#!/usr/bin/env python
import hashlib
import random
import urllib2
from BeautifulSoup import BeautifulSoup

def fetch_comic(comicname, fetch_timeout):
    comictitle = "Penny Arcade"

    try:
        url = 'https://www.penny-arcade.com/comic/'
        headers = { 'User-Agent' : 'Toonbot/1.0' }
        req = urllib2.Request(url, None, headers)
        site = urllib2.urlopen(req, timeout=fetch_timeout).read()
        soup = BeautifulSoup(site)
        div = (soup.find("div", attrs={'id':'comicFrame'}))
        title = div.find("img")["alt"].encode('utf8')
        comic = div.find("img")["src"].encode('utf8')
        link = (soup.find("meta", attrs={'property':'og:url'})["content"]).encode('utf8')
        prehash = comic
        hash = hashlib.md5()
        hash.update(prehash)
        comichash = hash.hexdigest()
        text = None
        return (True, comichash, title, comic, text, link, comicname, comictitle)

    except Exception, e:
        return (False, None, None, None, None, None, comicname, comictitle)
