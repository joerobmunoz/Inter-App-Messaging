__author__ = 'Joe Munoz'

import datetime


class Message():
    def __init__(self, sender="default", application="default", message=""):
        self.sender = sender
        self.application = application
        self.message = message
        self.creation_time = str(datetime.datetime.now())

    def fill_from_db(self, row):
        self.id = row[0]
        self.sender = row[1]
        self.application = row[2]
        self.message = row[3]
        self.creation_time = row[4]
