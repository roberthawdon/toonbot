from __main__ import *
import os
import os.path
import subprocess
from rtmbot.core import Plugin, Job

script_dirpath = os.path.dirname(os.path.join(os.getcwd(), __file__))

class FetchComicJob(Job):
    def run (self, slack_client):
        subprocess.Popen(script_dirpath + '/subprocesses/fetch-comics.py')
        return []

class FetchComics(Plugin):
    def register_jobs(self):
        job = FetchComicJob(3600)
        self.jobs.append(job)
