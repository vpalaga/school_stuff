import random
import os, sys
import pygame

def resource_path(relative:str):
    base = str(getattr(sys, '_MEIPASS', os.path.dirname(__file__)))
    return os.path.join(base, relative)

class Pos:
    def __init__(self, x:int|float, y:int|float):
        self.x = x
        self.y = y
        self.pos = (x, y)

    def __add__(self, other):
        if isinstance(other, Pos):
            new = Pos(self.x + other.x, self.y + other.y)
            return new
        return NotImplemented
    def __eq__(self, other):
        if isinstance(other, Pos):
            if self.x == other.x and self.y == other.y:
                return True
        return False
    def __neg__(self):
        return Pos(-self.x, -self.y)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Pos(self.x / other, self.y / other)
        return NotImplemented

    def __round__(self, n=None):
        return Pos(round(self.x, n), round(self.y, n))

    def __repr__(self):
        return f"({self.x}, {self.y})"


class Snake:
    def __init__(self, fieldSize:tuple[float|int,float|int]):

        self.length = 5
        self.heading = Pos(1, 0)
        self.headPos = Pos(5, 9)
        self.pos: list[Pos] = self._generateStartPos()

        self.img = self._loadHead(*fieldSize)

    def _generateStartPos(self)->list[Pos]:
        snake = []
        segment = self.headPos
        for n in range(self.length):
            snake.append(segment)
            segment = segment + -self.heading
        return snake

    @staticmethod
    def _loadHead(w:int, h:int)->pygame.Surface:
        img = pygame.image.load(resource_path("images/billeter.png")).convert_alpha()
        img = pygame.transform.scale(img, (w, h))
        return img

class Apple:
    sprites = []
    def __init__(self, pos: Pos):
        if len(Apple.sprites) == 0:
            raise Warning("sprites weren't loaded")

        self.pos = pos
        self.imageIndex = random.randint(0, len(Apple.sprites) - 1)
        self.img = self.sprites[self.imageIndex]

    @staticmethod
    def loadAppleSprites(w:float|int, h:float|int):
        sprites = []

        directory = resource_path(r"images/apples")
        for filename in os.listdir(directory):
            img = pygame.image.load(os.path.join(directory, filename)).convert_alpha()
            img = pygame.transform.scale(img, (w, h))
            sprites.append(img)

        Apple.sprites = sprites

class Tools:
    def __init__(self, gameSize: tuple[int,int], widowSize: tuple[int,int]):
        self.gameSize = gameSize
        self.windowSize = widowSize
        self.xField = self.windowSize[0] / self.gameSize[0]
        self.yField = self.windowSize[1] / self.gameSize[1]

    def isPosValid(self, p: Pos)->bool:
        if -1 < p.x < self.gameSize[0] and -1 < p.y < self.gameSize[1]:
            return True
        return False

    def randomPos(self)->Pos:
        return Pos(random.randint(0, self.gameSize[0] - 1),
                   random.randint(0, self.gameSize[1] - 1))

    def generateMidposDict(self)->dict[tuple[int,int], Pos]:
        midPos = {}

        yPush = self.yField / 2 + 100
        for y in range(self.gameSize[1]):
            xPush = self.xField / 2
            for x in range(self.gameSize[0]):
                midPos[(x, y)] = Pos(xPush, yPush)
                xPush += self.xField
            yPush += self.yField
        return midPos

    def translateCoords(self, p: Pos)->Pos:
        return Pos(p.x*self.xField + self.xField/2, p.y*self.yField + self.yField/2 + 100)

    @staticmethod
    def wherePosInApples(pos: Pos, apples: list[Apple])->int|None:
        for i in range(len(apples)):
            if apples[i].pos == pos:
                return i
        return None

class Colors:
    def __init__(self):
        self.darkGrass = (162, 209, 73)
        self.lightGrass= (170, 215, 81)
        self.apple =     (231, 71,  29)
        self.snake =     (72,  118, 236)
        self.background =(74 , 117, 44)
        self.title =     (181, 138, 211)
        self.score =     (255, 255, 255)
        self.tutorial =  (230, 230, 230)
