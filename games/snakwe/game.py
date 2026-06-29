from data import Pos, Snake, Tools
import random
class Game:
    def __init__(self, numOfSprites:int):
        self.numOfSprites = numOfSprites
        self.gameSize = (15, 15)
        self.windowSize = (600,600)
        self.applesOnScreen = 5
        self.fpsPerGametick = 15
        self.fps = 120

        self.score = 0

        self.tools = Tools(self.gameSize, self.windowSize)
        self.snake = Snake(self.gameSize)

        self.apples: dict[tuple[int,int], int] = {}
        for _ in range(self.applesOnScreen): self.spawnRndApple()
    def spawnRndApple(self)->None:
        while True:
            apple = self.tools.randomPos()

            if apple.pos in self.apples.keys(): continue
            elif apple in self.snake.pos: continue
            else:
                self.apples[int(apple.x), int(apple.y)] = random.randint(0,self.numOfSprites - 1)
                return

    def updateOnTick(self)->bool:
        """True all good, False: gameOver"""
        # clac new head pos
        newSnakeHeadPos = round(self.snake.headPos)
        # check for wall collision
        if not self.tools.isPosValid(newSnakeHeadPos):
            return False


        # snake colliding with itself
        if newSnakeHeadPos in self.snake.pos:
            return False
        # set new head
        self.snake.headPos = newSnakeHeadPos
        # add new head
        self.snake.pos.insert(0, newSnakeHeadPos)

        # remove tail if no apples eaten
        if newSnakeHeadPos.pos in self.apples.keys():
            # rem old apple
            del self.apples[newSnakeHeadPos.pos]
            self.spawnRndApple()
            self.score += 1
        else:
            self.snake.pos.pop(-1)

        return True