from gturtle import *
import math

makeTurtle()
hideTurtle()


def calc_delta(r, s, xy):
    pu()
    fd(r)
    pos1 = getPos()

    setPos(xy)
    rt(s)
    fd(r)
    pos2 = getPos()

    pd()
    return math.hypot(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))


def circle(r, a, xy=None, angle_step=1):
    if xy is not None:
        setPos(xy)
    else:
        xy = 0, 0

    d = calc_delta(r, angle_step, xy)

    rt(90)
    bk(d)

    for _ in range(a):
        fd(d)
        rt(angle_step)


rt(90)
circle(100, 180)