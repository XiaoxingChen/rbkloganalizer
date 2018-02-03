# Robokit log analyzer
    Python codes for robot motion analyze

# Table of Contents

    * [Requirements](#Requirements)
    * [Components](#Components)
        * [Log Ojects](#Log Objects)
    * [Yaw Comparer](#yaw Comparer)

# Requirements

- Python 3.6.x

- matplotlib

# Components
## Log Objects
This is a class for log objects.
For example, MCLoc information is a log object. Besides, IMU infomation, odometer infomations are also log objects.

# Yaw Comparer
This is an example for comparing the yaw angle from:
1. IMU log
2. Odometer log
3. Location after using laser

The confidence of the location will also be plotted on to the figure.
