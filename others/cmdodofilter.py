import re
import sys

if len(sys.argv) != 2:
    print('No input log file')
    input('press enter to exit...')
    quit()

log_file = sys.argv[1]
tail = log_file[-4:]
if tail != '.log':
    input('file format error: "' + tail + '", should be ".log"')
    quit()
