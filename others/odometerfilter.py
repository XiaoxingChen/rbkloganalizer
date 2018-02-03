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
odometer_list = re.findall(
    '.*\[Odometer\].*stamp: (\d*), x: (.*?), y: (.*?), angle: (.*?), stopped: (.*?)\n', log_file_str)

speedcmd_list = re.findall('X = (.*?),.* ts = (\d*)\n', log_file_str)

log_file.close()

time_stamp_offset_ns = float(odometer_list[100][0])
print('time offset = %dns' % time_stamp_offset_ns)

cmd_vx_mps = []
cmd_t_ms = []
for cmd in speedcmd_list:
    tempT = (float(cmd[1]) - time_stamp_offset_ns) / 1000000
    if(tempT < -1e10):
        print('invalid command point:' + str(cmd))
        continue
    cmd_t_ms += [tempT]
    cmd_vx_mps += [float(cmd[0])]


# print(cmd_t_ms)

t_ms = []
x_m = []
y_m = []
theta_rad = []
vx_mps = [0]
vy_mps = [0]
v_mps = [0]
for v in odometer_list:
    tempT = (float(v[0]) - time_stamp_offset_ns) / 1000000
    if(tempT < -1e10):
        print('invalid odom point:' + str(v))
        continue
    t_ms += [tempT]
    x_m += [float(v[1])]
    y_m += [float(v[2])]
    if(len(x_m) > 1):
        vx_mps += [(x_m[-1] - x_m[-2]) / (t_ms[-1] - t_ms[-2]) * 1000]
        vy_mps += [(y_m[-1] - y_m[-2]) / (t_ms[-1] - t_ms[-2]) * 1000]
        v_mps += [(vx_mps[-1]**2 + vy_mps[-1]**2)**0.5]
        if vx_mps[-1] < 0:
            v_mps[-1] *= -1
# print(t_ms)
# print(speedcmd_list)
# plt.plot(t_ms, x_m)
# plt.plot(t_ms, v_mps)
# plt.plot(t_ms, vx_mps)
# plt.plot(x_m, y_m)
# plt.plot(t_ms, x_m, t_ms, y_m)
# plt.plot(t_ms, x_m, t_ms, v_mps)
# plt.plot(cmd_t_ms, cmd_vx_mps)
plt.plot(t_ms, vx_mps, cmd_t_ms, cmd_vx_mps, '.')
plt.show()
