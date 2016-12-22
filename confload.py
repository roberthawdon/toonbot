#!/usr/bin/env python
import sys
import os
import yaml

script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))

def ToonbotConf():
    config = yaml.load(open( script_dirpath + '/toonbot.conf', 'r'))
    return config
