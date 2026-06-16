class Point:
    def __init__(self, x:float|int, y:float|int)->None:
        self.x = x
        self.y = y
class Solve:
    def __init__(self):
        self.cuts = []
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
