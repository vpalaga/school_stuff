import math

POINTS = [(7.75, 0), (18,1), (23,2), (28,9), (33,4), (37.75, 1)]

def f(x:float, a:float, b:float, c:float)->float:
    return c * (pow(math.e, -b * pow(x - a, 2)))

def diff(a:float, b:float,c:float)->float:
    diffs = []
    for point in POINTS:
        diffs.append(abs(f(point[0], a, b, c) - point[1]))
    return sum(diffs)

vls = 0, 0, 0
mns = 1000000
ct = 0
for a in range(0, 1000):
    a /= 1000

    for b in range(0, 1000):
        b /= 10

        for c in range(0, 1000):
            c/=10

            clc = diff(a, b, c)

            if clc < mns:
                mns = clc
                vls = a, b, c

            print(f"{ct} : {1000 * 1000 * 1000}")
            ct += 1

print(vls)
