from __main__ import *
import os
import os.path
import subprocess

script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))

crontable = []
crontable.append([3600, "fetch_comics"])
outputs = []


def fetch_comics():

    subprocess.Popen(script_dirpath + '/subprocesses/fetch-comics.py')
