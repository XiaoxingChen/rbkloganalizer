import re
import sys
import matplotlib.pyplot as plt
from time import clock
import math
import matplotlib.dates as mdates
from components.objlog import LocLog
from components.objlog import OdomLog
from components.objlog import ImuLog
# import components.rbkkeywordparser
if len(sys.argv) != 2:
    print('No input log file')
    input('press enter to exit...')
    quit()

file_name = sys.argv[1]
tail = file_name[-4:]
if tail != '.log':
    input('file format error: "' + tail + '", should be ".log"')
    quit()

starttime = clock()

log_file = open(file_name, 'r', encoding='utf-8')
# log_file_str = log_file.read()

print('Read file cost time: %fs' % (clock() - starttime))
starttime = clock()

loglist = [LocLog(), OdomLog(), ImuLog()]

print('Findall in file...')
cnt = 0
for line in log_file:
    for obj in loglist:
        if(re.match(obj.expression, line) is not None):
            obj.matchlist += [re.match(obj.expression, line).groups()]
            cnt += 1
            if(0 == cnt % 1000):
                sys.stdout.write('.')
                sys.stdout.flush()
            continue
print('\nGrep match finished, cost time %fs...' % (clock() - starttime))
starttime = clock()

loc = loglist[0].parse()
loc_t = loc[0]
loc_theta = loc[3]

odom = loglist[1].parse()
odom_t = odom[0]
theta_rad = odom[3]

(yaw_t, yaw) = loglist[2].parse()

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))
# Plot
plt.plot(yaw_t, yaw, 'y-', odom_t, theta_rad, 'b', loc_t, loc_theta, 'r')
# plt.plot(loc_t, loc_theta, 'b', odom_t, theta_rad, 'r')
plt.gcf().autofmt_xdate()  # 自动旋转日期标记

print('plot cost time: %fs' % (clock() - starttime))
starttime = clock()
plt.show()
