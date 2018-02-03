import re
import sys
import matplotlib.pyplot as plt

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
log_file_str = log_file.read()
tstamp_list = re.findall(
    'timestamp: (\d.*?), receive_t: (\d.*?),.*\n', log_file_str)


log_file.close()

delta_t = []

for tt in tstamp_list:
    delta_t += [int(tt[1]) - int(tt[0])]

print(delta_t)
