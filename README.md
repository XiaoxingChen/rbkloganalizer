# Robokit log analyzer
Python codes for robot motion analyze

# Table of Contents

   * [Requirements](#Requirements)
   * [Components](#Components)
      * [Log Ojects](#log-objects)
   * [Yaw Comparer](#yaw-comparer)
   * [IMU Detail](#imu-detail)

# Requirements

- Python 3.6.x

- matplotlib

# Components
## Log Objects
This is a class for log objects.
For example, MCLoc information is a log object. Besides, IMU infomation, odometer infomations are also log objects.

# Yaw Comparer

![example](https://github.com/XiaoxingChen/rbkloganalizer/blob/master/yawcomparer/compareEx.png)

This is an example for comparing the yaw angle from:
1. IMU log
2. Odometer log
3. Location after using laser

The confidence of the location will also be plotted on to the figure.

# IMU Detail

![example](https://github.com/XiaoxingChen/rbkloganalizer/blob/master/imudetail/detailEx.png)

There are three subplots in IMU details.
1. The compensated acceleration in three axis of the acceleration sensor
2. The rotate velocity in three axis of the gyroscope
3. The acceleration offset

