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
        self.result = [[0]] * 5
        self.expression = '\[(.*?)\]\[MCLoc\].*x:(.*?):y:(.*?):theta:(.*?):confidence:(.*)\n'

    def parse(self):
        if(len(self.matchlist) == 0):
            return

        t0 = clock()
        raw = [(rbktimetodate(v[0]), float(v[1]), float(v[2]),
                float(v[3]) * math.pi / 180, float(v[4]))for v in self.matchlist]
        ret = list(zip(*raw))
        ret[3] = list(ret[3])
        anglejoint(ret[3])
        self.result = ret
        print('MCLoc keyword parse finished, cost %fs...' % (clock() - t0))
        return ret

    def t(self):
        return self.result[0]

    def x(self):
        return self.result[1]

    def y(self):
        return self.result[2]

    def theta(self):
        return self.result[3]

    def confidence(self):
        return self.result[4]


class OdomLog(object):
    def __init__(self):
        self.matchlist = []
        self.result = [[0]] * 5
        self.expression = '.*\[Odometer\].*stamp: (\d*), x: (.*?), y: (.*?), angle: (.*?), stopped: (.*?)\n'

    def parse(self):
        if(len(self.matchlist) == 0):
            return

        t0 = clock()

        raw = [(datetime.fromtimestamp(float(v[0]) / 1e9), float(v[1]),
                float(v[2]), float(v[3]), (v[4] is 'true'))
               for v in self.matchlist if timestampvalid(v[0])]
        ret = list(zip(*raw))
        ret[3] = list(ret[3])
        anglejoint(ret[3])
        self.result = ret
        print('Odometer keyword parse finished, cost %fs...' % (clock() - t0))
        return ret

    def t(self):
        return self.result[0]

    def x(self):
        return self.result[1]

    def y(self):
        return self.result[2]

    def theta(self):
        return self.result[3]

    def stopped(self):
        return self.result[4]


class ImuLog(object):
    def __init__(self):
        self.matchlist = []
        self.result = [[0]] * 2
        self.expression = '.*yaw: (.*?), timestamp: (.*?)\n'
        # self.expression = '.*yaw: (.*?)timestamp: (.*?)\n'

    def parse(self):
        if(len(self.matchlist) == 0):
            print('No data match for IMU')
            return

        t0 = clock()
        raw = [(datetime.fromtimestamp(float(v[1]) / 1e9), float(v[0]))
               for v in self.matchlist if timestampvalid(v[1])]
        ret = list(zip(*raw))

        ret[1] = list(ret[1])
        anglejoint(ret[1])
        self.result = ret
        print('IMU keyword parse finished, cost %fs...' % (clock() - t0))
        return ret

    def t(self):
        return self.result[0]

    def theta(self):
        return self.result[1]


class ImuDetailLog(object):
    def __init__(self):
        self.matchlist = []
        self.result = [[0]] * 9
        self.expression = 'acc = \[(.*?), (.*?), (.*?)]w = \[(.*?), (.*?), (.*?)];off = \[(.*?), (.*?), (.*?)]\n'

    def parse(self):
        if(len(self.matchlist) == 0):
            return

        t0 = clock()
        raw = [(float(v[0]), float(v[1]), float(v[2]), float(v[3]),
                float(v[4]), float(v[5]), float(v[6]), float(v[7]), float(v[8]))
               for v in self.matchlist]

        ret = list(zip(*raw))

        self.result = ret

        print('Error code parse finished, cost %fs...' % (clock() - t0))
        return ret

    def accx(self):
        return self.result[0]

    def accy(self):
        return self.result[1]

    def accz(self):
        return self.result[2]

    def rotx(self):
        return self.result[3]

    def roty(self):
        return self.result[4]

    def rotz(self):
        return self.result[5]

    def offx(self):
        return self.result[6]

    def offy(self):
        return self.result[7]

    def offz(self):
        return self.result[8]


class ErrorCodeLog(object):
    def __init__(self):
        self.matchlist = []
        self.expression = '\[(.*?)].*\[info]\[ErrorCode.*?] (.*?):'

    def parse(self):
        if(len(self.matchlist) == 0):
            input('No keyword match, please check the grep!')
            return

        t0 = clock()
        ret = [(rbktimetodate(v[0]), v[1], float(v[1][1:]) / 1e5)
               for v in self.matchlist]
        # ret = list(zip(*raw))

        print('Error code parse finished, cost %fs...' % (clock() - t0))
        return ret


class CommandLog(object):
    def __init__(self):
        self.matchlist = []
        self.result = [[0]] * 4
        self.expression = '\[(.*?)].*{ "vx" : (.*?), "vy" : (.*?), "w" : (.*?) }\n'

    def parse(self):
        if(len(self.matchlist) == 0):
            return

        # print(self.matchlist)
        t0 = clock()
        raw = [(rbktimetodate(v[0]), float(v[1]), float(v[2]),
                float(v[3]) * 10)for v in self.matchlist]
        ret = list(zip(*raw))

        self.result = ret
        print('Velocity command keyword parse finished, cost %fs...' %
              (clock() - t0))
        return ret

    def omega(self):
        return self.result[3]

    def t(self):
        return self.result[0]
