#!/usr/bin/env python
class commitMeta:
    isPorted = False

    def __init__(self,commit_number=None,author=None,date=None,message=None):
        self.commitNumber = commit_number
        self.author = author
        self.date = date
        self.message = message

    def __repr__(self):
        return "Commit : {0}\n Author : {1} \n Date: {2} \n{3}\n".format(
                             self.commitNumber,self.author,self.date,self.message)

    def setCommitNumber(self,commit_number):
        self.commitNumber = commit_number

    def setAuthor(self,author):
        self.author = author

    def setDate(self,date):
        self.date = date

    def setMessage(self,message):
        self.message = message

class commitDB:
    def __init__(self,commits):
        self.commits = commits

