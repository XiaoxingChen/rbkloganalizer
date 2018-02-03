import re
import sys

import matplotlib.pyplot as plt
from time import clock
import math
import matplotlib.dates as mdates
sys.path.append('../')
from components.objlog import LocLog
from components.objlog import OdomLog
from components.objlog import ImuLog

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
loc_conf = loc[4]

odom = loglist[1].parse()
odom_t = odom[0]
theta_rad = odom[3]

(yaw_t, yaw) = loglist[2].parse()

# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))

fig = plt.figure()
ax1 = fig.add_subplot(111)

# Plot
ax1.plot(yaw_t, yaw, 'y-', label='imu')
ax1.plot(odom_t, theta_rad, 'k', label='odom')
ax1.plot(loc_t, loc_theta, 'r', label='loc')
ax1.set_ylabel('Yaw/rad (1deg = 0.017rad)')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))
ax1.legend()
fig.autofmt_xdate()

ax2 = ax1.twinx()
ax2.plot(loc_t, loc_conf, 'b', label='confidence', alpha=0.5)
ax2.set_ylabel('Confidence')
ax2.set_xlabel('Time')
ax2.legend()

# plt.gcf().autofmt_xdate()  # 自动旋转日期标记

print('plot cost time: %fs' % (clock() - starttime))
starttime = clock()

plt.title('Yaw comparer')


# plt.legend()
plt.show()
