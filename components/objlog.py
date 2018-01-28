# from rbkkeywordparser import timestampvalid
# from rbkkeywordparser import anglejoint
# from rbkkeywordparser import rbkstamptodate
# from rbkkeywordparser import rbktimetodate

from time import clock
import re
from datetime import datetime
import math


def rbktimetodate(rbktime):
    return datetime.strptime(rbktime, '%Y-%m-%d %H:%M:%S.%f')


def rbkstamptodate(rbkstamp):
    return datetime.fromtimestamp(float(rbkstamp) / 1e9)


def timestampvalid(ts):
    return float(ts) * 1e-9 > datetime.timestamp(datetime(2000, 1, 1))


def anglejoint(anglelist):
    base_offset = anglelist[0]
    anglelist[0] = 0
    increase_offset = 0
    for i in range(1, len(anglelist)):
        temp = anglelist[i] + increase_offset
        if(temp - anglelist[i - 1] > math.pi):
            increase_offset -= 2 * math.pi
        elif (temp - anglelist[i - 1] < -math.pi):
            increase_offset += 2 * math.pi

        anglelist[i] = anglelist[i] + increase_offset - base_offset


class LocLog(object):
    def __init__(self):
        self.matchlist = []
        self.expression = '\[(.*?)\]\[MCLoc\].*x:(.*?):y:(.*?):theta:(.*?):confidence:(.*)\n'

    def parse(self):
        if(len(self.matchlist) == 0):
            input('No keyword match, please check the grep!')
            return

        t0 = clock()
        raw = [(rbktimetodate(v[0]), float(v[1]), float(v[2]),
                float(v[3]) * math.pi / 180, float(v[4]))for v in self.matchlist]
        ret = list(zip(*raw))
        ret[3] = list(ret[3])
        anglejoint(ret[3])
        print('MCLoc keyword parse finished, cost %fs...' % (clock() - t0))
        return ret


class OdomLog(object):
    def __init__(self):
        self.matchlist = []
        self.expression = '.*\[Odometer\].*stamp: (\d*), x: (.*?), y: (.*?), angle: (.*?), stopped: (.*?)\n'

    def parse(self):
        if(len(self.matchlist) == 0):
            input('No keyword match, please check the grep!')
            return

        t0 = clock()

        raw = [(datetime.fromtimestamp(float(v[0]) / 1e9), float(v[1]),
                float(v[2]), float(v[3]), (v[4] is 'true'))
               for v in self.matchlist if timestampvalid(v[0])]
        ret = list(zip(*raw))
        ret[3] = list(ret[3])
        anglejoint(ret[3])
        print('Odometer keyword parse finished, cost %fs...' % (clock() - t0))
        return ret


class ImuLog(object):
    def __init__(self):
        self.matchlist = []
        self.expression = '.*yaw: (.*?), timestamp: (.*?)\n'

    def parse(self):
        if(len(self.matchlist) == 0):
            input('No keyword match, please check the grep!')
            return

        t0 = clock()
        raw = [(datetime.fromtimestamp(float(v[1]) / 1e9), float(v[0]))
               for v in self.matchlist if timestampvalid(v[1])]
        ret = list(zip(*raw))

        ret[1] = list(ret[1])
        anglejoint(ret[1])
        print('IMU keyword parse finished, cost %fs...' % (clock() - t0))
        return ret
