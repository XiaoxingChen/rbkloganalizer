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
from components.objlog import ImuDetailLog

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

logd = {'loc': LocLog(), 'odom': OdomLog(), 'imu': ImuLog(),
        'imud': ImuDetailLog()}

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

fig = plt.figure(1)
fig.suptitle("IMU detail analyze", fontsize=18)

ax1 = fig.add_subplot(311)

# Plot Acc
ax1.plot(logd['imu'].t(), logd['imud'].accx(),
         'r', label='ax', linewidth=0.5)
ax1.plot(logd['imu'].t(), logd['imud'].accy(),
         'g', label='ay', linewidth=0.5)
ax1.plot(logd['imu'].t(), logd['imud'].accz(),
         'b', label='az', linewidth=0.5)

ax1.set_ylabel('$Acc (m/s^2)$')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))
plt.setp(ax1.get_xticklabels(), visible=False)
ax1.legend()

# Plot Rot
ax2 = fig.add_subplot(312, sharex=ax1)
ax2.plot(logd['imu'].t(), logd['imud'].rotx(),
         'r', label='wx', linewidth=0.5)
ax2.plot(logd['imu'].t(), logd['imud'].roty(),
         'g', label='wy', linewidth=0.5)
ax2.plot(logd['imu'].t(), logd['imud'].rotz(),
         'b', label='wz', linewidth=0.5)

ax2.set_ylabel('Rot (rad/s)')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))
plt.setp(ax2.get_xticklabels(), visible=False)
ax2.legend()


# Plot Rot
ax3 = fig.add_subplot(313, sharex=ax1)
ax3.plot(logd['imu'].t(), logd['imud'].offx(),
         'r', label='offx', alpha=0.8)
ax3.plot(logd['imu'].t(), logd['imud'].offy(),
         'g', label='offy', alpha=0.8)
ax3.plot(logd['imu'].t(), logd['imud'].offz(),
         'b', label='offz', alpha=0.8)

ax3.set_ylabel('Rot offset (rad/s)')
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S.%f'))
plt.setp(ax2.get_xticklabels(), visible=False)
ax3.legend()

fig.autofmt_xdate()

print('plot cost time: %fs' % (clock() - starttime))
starttime = clock()

# plt.legend()
plt.show()
