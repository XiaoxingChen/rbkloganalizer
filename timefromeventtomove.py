import re
import sys
import matplotlib.pyplot as plt
import time
import math

if len(sys.argv) != 2:
    print('No input log file')
    input('press enter to exit...')
    quit()

file_name = sys.argv[1]
tail = file_name[-4:]
if tail != '.log':
    input('file format error: "' + tail + '", should be ".log"')
    quit()

log_file = open(file_name, 'r', encoding='utf-8')
# log_file_str = log_file.read()

odom_match_str = '\[(.*?)\.(.*?)\].*\[Odometer\].*pped: (.*)\n'
gotarget_match_str = '\[(.*?)\.(.*?)\].*go_target.*col # \((\d*),.*\n'

prevstopped = True
# startmoveflag = False
waittomove = False
gocommandtime = 0
prevgocommand = ''

for line in log_file:
    matchobj = re.search(odom_match_str, line, flags=0)

    if matchobj is not None:
        if (matchobj.group(3) == 'false' and prevstopped is True and waittomove is True):
            timeArray = time.strptime(matchobj.group(
                1), "%Y-%m-%d %H:%M:%S")
            tempT = time.mktime(timeArray) + float('0.' + matchobj.group(2))
            delta_time = tempT - gocommandtime

            print('dt = %.3fs, t0 = %.3fs, t1 = %.3fs,\ngocmd: %s,startmove: %s ' % (
                delta_time, gocommandtime, tempT, prevgocommand, matchobj.group(0)))
            waittomove = False

        if(matchobj.group(3) == 'true'):
            prevstopped = True
        else:
            prevstopped = False

    matchobj = re.search(gotarget_match_str, line, flags=0)
    if matchobj is not None:
        timeArray = time.strptime(matchobj.group(1), "%Y-%m-%d %H:%M:%S")
        tempT = time.mktime(timeArray) + float('0.' + matchobj.group(2))
        gocommandtime = tempT
        waittomove = True
        prevgocommand = matchobj.group(0)
