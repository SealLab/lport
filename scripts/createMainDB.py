#!/usr/bin/env python
import sys
import argparse
import shlex
import os
import subprocess
import sys
import pickle
import csv
import re
from datetime import *
from MainLogDB import *

class mainParser:
    mainLogFile = ""
    commits = []
    count = 0
    logMsg = ""

    def __init__(self, m_file):
        self.mainLogFile = os.path.abspath(m_file)

    def reset(self):
        self.count += 1
        self.logStart = False
        self.logMsg = ""

    def parse(self):
        for line in open(self.mainLogFile):
            if line.startswith("commit "):

                self.parse_src_log()
                self.reset()

            self.logMsg += line

        self.parse_src_log()


    def parse_src_log(self):
       # print self.logMsg
        cm = commitMeta()
        log = self.logMsg.split("\n")
        msg = ""
        print log
        for line in log:
            if line.startswith("commit "):
                cm_no = line.split("commit ")[1]
                cm.setCommitNumber(cm_no)
            elif line.startswith("Author: "):
                auth = line.split("Author: ")[1]
                cm.setAuthor(auth)
            elif line.startswith("Date: "):
                date = line.split("Date: ")[1]
                cm.setDate(date)
            else:
                msg += line + "\n"

        cm.setMessage(msg)
        self.commits.append(cm)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parsing Linux mainline log and stroring it to a database')
    parser.add_argument('-m',action="store", dest='main_log',help="main line log files")
    parser.add_argument('-o',action='store', dest='out_file', default='main_db.pckl', help="output file where parsed log will be strored")

    args = parser.parse_args()

    print 'Main Logs        =', args.main_log
    print 'Output File        =', args.out_file


    if os.path.isfile(args.main_log) is False:
        print "!!main log file does not exist"
        sys.exit()


    fp = mainParser(args.main_log)
    fp.parse()
    for cm in fp.commits:
        print cm

    main_db = commitDB(fp.commits)

    pickle.dump( main_db, open( args.out_file, "wb" ) )

