#!/usr/bin/env python
import hashlib
import random
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup

def fetch_comic(comicname, fetch_timeout):
    comictitle = "Cyanide and Happiness"

    try:
        url = 'http://explosm.net/comics/latest/'
        headers = { 'User-Agent' : 'Toonbot/1.0' }
        req = urllib2.Request(url, None, headers)
        site = urllib2.urlopen(req, timeout=fetch_timeout).read()
        soup = BeautifulSoup(site)
        comicurl = "http:" + (soup.find("img", attrs={'id':'main-comic'})["src"]).encode('utf8')
        comic = urllib.quote(comicurl, safe=':/?=&')
        link = (soup.find("input", attrs={'id':'permalink'})["value"]).encode('utf8')
        prehash = comic
        hash = hashlib.md5()
        hash.update(prehash)
        comichash = hash.hexdigest()
        title = None
        if "Thumbnail" in comic:
            text = "To view this Cyanide and Happiness video, go to: " + link
        else:
            text = None
        return (True, comichash, title, comic, text, link, comicname, comictitle)

    except Exception, e:
        return (False, None, None, None, None, None, comicname, comictitle)
