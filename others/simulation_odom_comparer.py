import re
import sys
import matplotlib.pyplot as plt
from time import clock
import math

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
log_file_str = log_file.read()

print('Read file cost time: %fs' % (clock() - starttime))
starttime = clock()

expression = 't: (.*?), vx: (.*?), predodom \[(.*?), (.*?), (.*?)\], odom \[(.*?), (.*?), (.*?)\]\n'
log_list = re.findall(expression, log_file_str)
t = [float(v[0]) for v in log_list]
vx = [float(v[1]) for v in log_list]
predx = [float(v[2]) for v in log_list]
predy = [float(v[3]) for v in log_list]
predthera = [float(v[4]) for v in log_list]
odox = [float(v[5]) for v in log_list]
odoy = [float(v[6]) for v in log_list]
odothera = [float(v[7]) for v in log_list]

print('Findall in file...')


print('plot cost time: %fs' % (clock() - starttime))

# plt.plot(t, predx, 'r', t, odox, 'b')
plt.plot(predx, predy, 'r', odox, odoy, 'b')

starttime = clock()
plt.show()
