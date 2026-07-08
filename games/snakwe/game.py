from operator import pos

from data import Snake, Tools, Apple, resource_path, Wall, Pos
import pygame, random

class Game:
    sound = True
    def __init__(self):
        self.gameSize = (20, 20)
        self.windowSize = (700,700)
        self.applesOnScreen = 3
        self.fpsPerGametick = 15
        self.fps = 120
        self.wallSpawn = 1
        self.maxWalls = 20
        self.smallestSpawnDistance = 3

        self.score = 0
        self.tick = 0

        self.tools = Tools(self.gameSize, self.windowSize)
        self.snake = Snake((self.tools.xField * 1.3, self.tools.yField * 1.3))

        self.apples: list[Apple] = []
        Apple.loadAppleSprites(self.tools.xField * 1.2, self.tools.yField * 1.2)
        Apple.loadSounds()

        self.walls: list[Wall] = []
        self.lastWallSpawnTick = 0

        for _ in range(self.applesOnScreen): self.spawnRndApple()

    def isPosFree(self, pos:Pos)->bool:
        if self.tools.wherePosInApples(pos, self.apples) is not None: return False
        if self.tools.wherePosInWalls(pos, self.walls) is not None: return False
        if self.snake.headPos.distanceTo(pos) < self.smallestSpawnDistance: return False
        if pos in self.snake.pos: return False
        return True


    def rndPos(self)->Pos|None:

        if self.gameSize[0] * self.gameSize[1] - len(self.snake.pos) - len(self.apples) - len(self.walls) <= 0:
            return None

        # brute a pos that satisfies all reqs.
        while True:
            pos = self.tools.randomPos()
            if self.isPosFree(pos):
                return pos

    def spawnRndApple(self)->None:
        pos = self.rndPos()
        if pos is not None:
            self.apples.append(Apple(pos))

    def spawnRndWall(self)->None:

        if not (self.tick - self.lastWallSpawnTick > self.wallSpawn):
            return

        if len(self.walls) >= self.maxWalls:
            return

        if random.randint(0,2) != 0:
            return

        if len(self.walls) == 0 or random.randint(0,4) == 0:
            # single random wall somewhere
            pos = self.rndPos()
            if pos is not None:
                self.walls.append(Wall(pos))
                self.lastWallSpawnTick = self.tick
        else:
            # wall style of wall spawn
            while True:
                wall: Wall = random.choice(self.walls)
                newWallPos = wall.pos + self.tools.randomHeading()

                if not self.tools.isPosValid(newWallPos): continue
                if not self.isPosFree(newWallPos): continue
                if newWallPos.distanceTo(self.snake.headPos) < self.smallestSpawnDistance: continue
                break

            self.walls.append(Wall(newWallPos))


    def updateOnTick(self)->bool:
        """True all good, False: gameOver"""
        # spawn new walls
        self.spawnRndWall()

        # clac new head pos
        newSnakeHeadPos = round(self.snake.headPos)
        # check for wall collision
        if not self.tools.isPosValid(newSnakeHeadPos):
            return False

        # snake colliding with itself
        if newSnakeHeadPos in self.snake.pos:
            return False

        # wall touch
        touchedWallIndex = self.tools.wherePosInWalls(newSnakeHeadPos, self.walls)
        if touchedWallIndex is not None:
            return False

        # set new head
        self.snake.headPos = newSnakeHeadPos
        # add new head
        self.snake.pos.insert(0, newSnakeHeadPos)

        # remove tail if no apples eaten
        eatenAppleIndex = self.tools.wherePosInApples(newSnakeHeadPos, self.apples)
        if eatenAppleIndex is not None:
            # rem old apple
            apple = self.apples.pop(eatenAppleIndex)
            if self.sound:
                apple.sound.play(maxtime=3000)  # play only the first 3000 ms (3 seconds)

            self.spawnRndApple()
            self.score += 1

            # remove a wall for eaten apple
            if len(self.walls) > 0:
                self.walls.pop(0)

        else:
            self.snake.pos.pop(-1)

        self.tick += 1

        return True