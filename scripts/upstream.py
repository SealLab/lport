#!/usr/bin/env python
import sys
import argparse
import shlex
import os
import subprocess

class MainLineLog:
    commit_message = []
    isPorted = False

class fileParser:
    stableFile = ""
    mainFile = ""
    outFile = ""
    keyWords1 = []
    keyWords2 = []
    isSrcFile = False
    logStart = False
    logBuf = ""
    logWithKey1 = ""
    logWithKey2 = ""
    count = 0


    def __init__(self, s_file,m_file, out_file, keys1):
        self.stableFile = os.path.abspath(s_file)
        self.mainFile = os.path.abspath(m_file)
        self.outFile = os.path.abspath(out_file)
        self.keyWords1 = keys1

    def reset(self):
        self.isSrcFile = False
        self.reset1()

    def reset1(self):
        self.logStart = False
        self.logBuf = ""
        logWithKey1 = ""
        logWithKey2 = ""

    '''
        start parsing the Linux log files;
        dump the logs which will contain the key words:
        1. It'll look at only source/header files
        2. In those file logs, it'll look for keyWords1
        3. If keyWords1 is found, it'll then look for keyWords2
    '''

    def parse(self):
        self.fileOut = open(self.outFile,"w")

        self.fileOut.write('\nInput Log File     =' + self.stableFile)
        self.fileOut.write('\nOutput File        =' + self.outFile)
        self.fileOut.write('\nSearch key words1  = %r' % self.keyWords1)
#        self.fileOut.write('\nSearch key words2  = %r\n\n' % self.keyWords2)

        for line in open(self.stableFile):
            if line.startswith("commit "):
                self.parse_src_log(line)
                self.reset()
                self.fileOut.write("====================\n")

            self.logBuf += line

        self.parse_src_log(line)

    def search_for_key1(self):
        for key1 in self.keyWords1:
            if key1 in self.logBuf:
                self.logWithKey1 = self.logBuf
                return True

        return False

    def search_for_key2(self):
        for key2 in self.keyWords2:
            if key2 in self.logWithKey1:
                self.logWithKey2 = self.logWithKey1
                return True

        return False


    def parse_src_log(self,line):

        if self.search_for_key1():
            self.count += 1
        else:
            self.fileOut.write(self.logBuf + "\n")
                #print self.logBuf + "\n"

    def parse_rev_log(self,line):

        if self.logStart:
            #parsing each revision
            self.logBuf += line


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Checking backported commits in Linux stable branches')
    parser.add_argument('-s',action="store", dest='stable_log',help="stable log files")
    parser.add_argument('-m',action="store", dest='main_log',help="main line log files")
    parser.add_argument('-o',action='store', dest='out_file', default='parse.log', help="output file where parsed log will be strored")
    parser.add_argument('-k1', '--key1', nargs='+', help="search keywords in 1st parse")

    args = parser.parse_args()

    print 'Stable Logs      =', args.stable_log
    print 'Main Logs        =', args.main_log
    print 'Output File        =', args.out_file
    print 'Search key words1   =', args.key1

    if os.path.isfile(args.stable_log) is False:
        print "!!stable log file does not exist"
        sys.exit()

    if os.path.isfile(args.main_log) is False:
        print "!!main log file does not exist"
        sys.exit()


    fp = fileParser(args.stable_log,args.main_log,args.out_file,args.key1)
    fp.parse()

    print fp.count
