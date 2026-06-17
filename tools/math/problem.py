import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont


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

p = Point(1, 2)
print(p)

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
        self.cuts = []

        self.img = Image.new("RGB", (500, 500), color="white")
        self.draw = ImageDraw.Draw(self.img)

        self._prepImageBackground()

    def _prepImageBackground(self):
        self.draw.circle((250,250), 200, outline="black", width=3)

    def plotPoint(self, p:Point, c:str="red"):
        print(p.translated())
        self.draw.circle(p.translated(), 3, fill=c)
    def plotLine(self, l:Line, c:str="red")->None:
        start = l.p1.translated()
        end = l.p2.translated()
        self.plotPoint(l.p1)
        self.plotPoint(l.p2)
        self.draw.line((start, end), fill=c)
    def show(self):
        self.img.show()
    @staticmethod

    def do_cut(a: Point, b: Point, c: Point, d: Point) -> bool:
        rx = b.x - a.x
        ry = b.y - a.y

        sx = d.x - c.x
        sy = d.y - c.y

        denom = rx * sy - ry * sx  # cross-product r × s

        if denom == 0:
            return False  # parallel or collinear

        wx = c.x - a.x
        wy = c.y - a.y

        t = (wx * sy - wy * sx) / denom
        u = (wx * ry - wy * rx) / denom

        return 0 <= t <= 1 and 0 <= u <= 1

if __name__ == "__main__":
    s = Solve(100)
    for _ in range(20):
        s.plotLine(Line())
    s.show()
