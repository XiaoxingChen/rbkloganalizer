import matplotlib.pyplot as plt

filename = 'yaw.txt'
f = open(filename, 'r')
yaw = []
t = []
tt = 0
for line in f:
    yaw += [float(line)]
    tt = tt + 38
    t += [tt]

# print(yaw)
plt.plot(t, yaw, '.')
plt.show()
