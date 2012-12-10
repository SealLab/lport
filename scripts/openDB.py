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

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print "Usage: openDB.py main_db.pckl"
        sys.exit(2)

    main_db = pickle.load(open(sys.argv[1],"rb"))

    commits = main_db.commits

    for cm in commits:
        print cm



