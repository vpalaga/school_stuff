import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont
from itertools import permutations
import matplotlib.pyplot as plt
from statistics import mean


class Point:
    def __init__(self, x:float|int, y:float|int)->None:
        self.x = x
        self.y = y
    def __repr__(self):
        return f"{round(self.x, ndigits=2)} {round(self.y, 2)}"

    def translated(self)->tuple[float,float]:
        x = self.x * 200 + 250
        y = self.y * 200 + 250
        return x, 500 - y

class Line:
    def __init__(self)->None:
        self.p1 = self.randomPosOnCircle()
        self.p2 = self.randomPosOnCircle()

    @staticmethod
    def randomPosOnCircle()->Point:
        posOnCircle = np.random.uniform(0, 2 * np.pi)
        x = math.sin(posOnCircle)
        y = math.cos(posOnCircle)

        return Point(x, y)

class Solve:
    def __init__(self, lines:int)->None:
        self.lines_n = lines
        self.lines: list[Line] = []

        # for n lines: num of cuts
        self.cuts: dict[int,int] = {}

        self.img = Image.new("RGB", (500, 500), color="white")
        self.draw = ImageDraw.Draw(self.img)

        self._prepImageBackground()

    def _prepImageBackground(self):
        self.draw.circle((250,250), 200, outline="black", width=3)

    def plotPoint(self, p:Point, c:str="red"):
        self.draw.circle(p.translated(), 3, fill=c)

    def plotLine(self, l:Line, c:str="red")->None:
        start = l.p1.translated()
        end = l.p2.translated()
        self.plotPoint(l.p1)
        self.plotPoint(l.p2)
        self.draw.line((start, end), fill=c)
    @staticmethod
    def plotDict(d: dict):
        xs = list(d.keys())
        ys = list(d.values())

        plt.plot(xs, ys, 'o-')  # 'o-' = points + lines between them

        plt.margins(0.1)  # 10% padding around the data
        plt.tight_layout()  # fit everything into the window
        plt.show()

    def show(self):
        self.img.show()

    @staticmethod
    def do_cut(l1:Line, l2:Line) -> None|Point:
        a, b = l1.p1, l1.p2
        c, d = l2.p1, l2.p2

        rx = b.x - a.x
        ry = b.y - a.y

        sx = d.x - c.x
        sy = d.y - c.y

        denom = rx * sy - ry * sx

        if denom == 0:
            return None  # parallel

        wx = c.x - a.x
        wy = c.y - a.y

        t = (wx * sy - wy * sx) / denom
        u = (wx * ry - wy * rx) / denom

        if 0 <= t <= 1 and 0 <= u <= 1:
            return Point(a.x + t * rx, a.y + t * ry)  # intersection point
        return None

    def simulate(self)->None:
        for n in range(1,self.lines_n+1):
            newLine = Line()
            self.lines.append(newLine)
            self.plotLine(newLine)

        cutsCount = 0
        for line1, line2 in permutations(self.lines, 2):
            ret = self.do_cut(line1, line2)
            if ret is not None:
                #self.plotPoint(ret, c="blue")
                cutsCount+=0.5
        self.cuts[0] = round(cutsCount)


def simulation():
    results:list[int] = []
    for n in range(100000):
        solve = Solve(100)
        solve.simulate()
        results.append(list(solve.cuts.values())[-1])

    results.sort()
    print(f"avg: {mean(results)}")

    result_data = {}
    for result in results:
        result_data[result] = results.count(result)

    print(result_data)

    plt.xlim(results[0] - 10, results[-1] + 10)  # x-axis range
    plt.bar(result_data.keys(), result_data.values(), width=0.8, color='steelblue', edgecolor='black')
    plt.margins(0.5)  # 10% padding around the data
    plt.tight_layout()  # fit everything into the window
    plt.show()


if __name__ == "__main__":
    simulation()

