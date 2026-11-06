import math

class Vec2:
    def __init__(self, x:float, y:float)->None:
        self.x = x
        self.y = y
        self.xy = (x, y)
    def __add__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x + other.x, self.y + other.y)
        else:
            return NotImplemented

    def __neg__(self):
        return Vec2(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, float):
            return Vec2(self.x * other, self.y * other)
        elif isinstance(other, int):
            return Vec2(self.x * other, self.y * other)
        elif isinstance(other,Vec2):
            return Vec2(self.x * other.x, self.y * other.y)
        return NotImplemented

    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"

    def __sub__(self, other):
        if isinstance(other, Vec2):
            return Vec2(self.x - other.x, self.y - other.y)
        return NotImplemented

    def len(self):
        return math.hypot(self.x, self.y)