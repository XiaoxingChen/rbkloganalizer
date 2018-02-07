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
from components.objlog import ErrorCodeLog
from components.objlog import ImuDetailLog
from components.objlog import CommandLog

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

loglist = [LocLog(), OdomLog(), ImuLog(), ErrorCodeLog()]
logd = {'loc': LocLog(), 'odom': OdomLog(), 'imu': ImuLog(),
        'imud': ImuDetailLog(), 'vcmd': CommandLog()}

print('Findall in file...')
cnt = 0
for line in log_file:
    for key in logd:
        if(re.match(logd[key].expression, line) is not None):
            logd[key].matchlist += [
                re.match(logd[key].expression, line).groups()]
            cnt += 1
            if(0 == cnt % 1000):
                sys.stdout.write('.')
                sys.stdout.flush()
            continue
print('\nGrep match finished, cost time %fs...' % (clock() - starttime))
starttime = clock()

for key in logd:
    logd[key].parse()

# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))

fig = plt.figure()
ax1 = fig.add_subplot(111)

# Plot
ax1.plot(logd['imu'].t(), logd['imu'].theta(), 'y-.', label='imu')
# ax1.plot(logd['odom'].t(), logd['odom'].x(), 'k-.', label='odom_x')
ax1.plot(logd['vcmd'].t(), logd['vcmd'].omega(), 'g.-',
         label='vcmd', markersize=0.8, linewidth=0.5)
ax1.plot(logd['odom'].t(), logd['odom'].theta(), 'k:', label='odom')
ax1.plot(logd['loc'].t(), logd['loc'].theta(), 'r--', label='loc')
ax1.plot(logd['odom'].t(), logd['odom'].stopped(),
         'b-', label='stopped', alpha=0.5, linewidth=0.5)

# ax1.plot(logd['imu'].t(), logd['imud'].accx(), 'y--', label='imu-accx')
ax1.set_ylabel('Yaw/rad (1deg = 0.017rad)')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))
ax1.legend()
fig.autofmt_xdate()

ax2 = ax1.twinx()
# ax2.plot(logd['loc'].t(), logd['loc'].confidence(),
#  'b', label='confidence', alpha=0.5)
ax2.set_ylabel('Confidence')
ax2.set_xlabel('Time')
ax2.legend()


# plt.gcf().autofmt_xdate()  # 自动旋转日期标记

print('plot cost time: %fs' % (clock() - starttime))
starttime = clock()

plt.title('Yaw comparer')


# plt.legend()
plt.show()
