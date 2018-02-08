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
log_file_str = log_file.read()
odometer_list = re.findall(
    '.*\[Odometer\].*stamp: (\d*), x: (.*?), y: (.*?), angle: (.*?), stopped: (.*?)\n', log_file_str)

confidence_list = re.findall(
    '\[(.*?)\..*\]\[.*confidence:(.*?)\n', log_file_str)

cmd_list = re.findall(
    '\[(.*?)\..*\].*"vx" : (.*?),.*"vy" : (.*?),.*"w" : (.*?) }\n', log_file_str)

yaw_list = re.findall('yaw: (.*?), timestamp: (.*?)\n', log_file_str)

log_file.close()

time_stamp_offset_ns = float(odometer_list[100][0])
print('time offset = %dns' % time_stamp_offset_ns)

wheelradius = 0.065
wheelphase = []

confi = []
confi_t_ms = []

for con in confidence_list:
    timeArray = time.strptime(con[0], "%Y-%m-%d %H:%M:%S")
    tempT = time.mktime(timeArray) * 1000.0 - time_stamp_offset_ns / 1000000.0
    if(tempT < -1e10):
        print('invalid confidence point:' + str(con))
        continue

    confi += [float(con[1])]
    confi_t_ms += [tempT]

cmd_w_radps = []
cmd_t_ms = []

# print(cmd_list)
w_pos = 3
vx_pos = 1
for cmd in cmd_list:
    timeArray = time.strptime(cmd[0], "%Y-%m-%d %H:%M:%S")
    tempT = time.mktime(timeArray) * 1000.0 - time_stamp_offset_ns / 1000000.0
    if(tempT < -1e10):
        print('invalid confidence point:' + str(cmd))
        continue

    # print(cmd[1])
    # sys.stdout.flush()
    cmd_w_radps += [float(cmd[w_pos])]
    cmd_t_ms += [tempT]

# print(cmd_t_ms)

yaw_rad = []
yaw_t_ms = []
rad_offset = 0
yaw_base_offset_rad = float(yaw_list[100][0])
for cmd in yaw_list:
    tempT = (float(cmd[1]) - time_stamp_offset_ns) / 1000000
    if(tempT < -1e10):
        print('invalid yaw point:' + str(cmd))
        continue
    yaw_t_ms += [tempT]
    if(len(yaw_rad) > 1):
        tempyaw = float(cmd[0]) + rad_offset
        if((tempyaw - yaw_rad[-1]) > math.pi):
            rad_offset -= 2 * math.pi
        elif ((tempyaw - yaw_rad[-1]) < -math.pi):
            rad_offset += 2 * math.pi

        yaw_rad += [float(cmd[0]) + rad_offset - yaw_base_offset_rad]
        # yaw_rad += [float(cmd[0])]
    else:
        yaw_rad += [float(cmd[0]) - yaw_base_offset_rad]


# print(cmd_t_ms)
t_ms = []
x_m = []
y_m = []
theta_rad = []
vx_mps = [0]
vy_mps = [0]
v_mps = [0]

rad_offset = 0
theta_base_offset_rad = float(odometer_list[100][3])
for v in odometer_list:
    tempT = (float(v[0]) - time_stamp_offset_ns) / 1000000
    if(tempT < -1e10):
        print('invalid odom point:' + str(v))
        continue
    t_ms += [tempT]
    x_m += [float(v[1])]
    y_m += [float(v[2])]
    wheelphase += [0.004 + 0.008 * math.sin(0.5 /
                                            wheelradius * (t_ms[-1] / 1000))]
    if(len(theta_rad) > 1):
        tempyaw = float(v[3]) + rad_offset
        if((tempyaw - theta_rad[-1]) > math.pi):
            rad_offset -= 2 * math.pi
        elif ((tempyaw - theta_rad[-1]) < -math.pi):
            rad_offset += 2 * math.pi

        theta_rad += [float(v[3]) + rad_offset - theta_base_offset_rad]
        # theta_rad += [float(v[3])]
    else:
        theta_rad += [float(v[3]) - theta_base_offset_rad]

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
# plt.plot(t_ms, vx_mps, cmd_t_ms, cmd_vx_mps, '.')
# plt.plot(t_ms, theta_rad, 'y', yaw_t_ms, yaw_rad, 'g',
#          confi_t_ms, confi, 'b', cmd_t_ms, cmd_w_radps, 'r')
# plt.plot(t_ms, wheelphase, 'y', t_ms, theta_rad, 'b')
plt.plot(t_ms, theta_rad, 'y.')
plt.show()
