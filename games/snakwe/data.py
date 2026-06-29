import random
class Pos:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
        self.pos = (x, y)

    def __add__(self, other):
        if isinstance(other, Pos):
            new = Pos(self.x + other.x, self.y + other.y)
            return new
        return None
    def __eq__(self, other):
        if isinstance(other, Pos):
            if self.x == other.x and self.y == other.y:
                return True
        return False
    def __neg__(self):
        return Pos(-self.x, -self.y)
    def __repr__(self):
        return f"({self.x}, {self.y})"


class Snake:
    def __init__(self, gameSize:tuple[int,int]):
        self.gameSize = gameSize

        self.length = 5
        self.heading = Pos(1, 0)
        self.headPos = Pos(5, 9)
        self.pos: list[Pos] = self._generateStartPos()

    def _generateStartPos(self)->list[Pos]:
        snake = []
        segment = self.headPos
        for n in range(self.length):
            snake.append(segment)
            segment = segment + -self.heading
        return snake

class Tools:
    def __init__(self, gameSize: tuple[int,int]):
        self.gameSize = gameSize

    def isPosValid(self, p: Pos)->bool:
        if -1 < p.x < self.gameSize[0] and -1 < p.y < self.gameSize[1]:
            return True
        return False

    def randomPos(self)->Pos:
        return Pos(random.randint(0, self.gameSize[0]),
                   random.randint(0, self.gameSize[1]))

if __name__ == "__main__":
    pass