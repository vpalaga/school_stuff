from data import Snake, Tools, Apple

class Game:
    def __init__(self):
        self.gameSize = (20, 20)
        self.windowSize = (700,700)
        self.applesOnScreen = 5
        self.fpsPerGametick = 15
        self.fps = 120

        self.score = 0

        self.tools = Tools(self.gameSize, self.windowSize)
        self.snake = Snake((self.tools.xField * 1.3, self.tools.yField * 1.3))

        self.apples: list[Apple] = []
        Apple.loadAppleSprites(self.tools.xField * 1.2, self.tools.yField * 1.2)

        for _ in range(self.applesOnScreen): self.spawnRndApple()

    def spawnRndApple(self)->None:
        while True:
            apple = self.tools.randomPos()

            if self.tools.wherePosInApples(apple, self.apples) is not None: continue

            elif apple in self.snake.pos: continue
            else:
                self.apples.append(Apple(apple))
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
        eatenAppleIndex = self.tools.wherePosInApples(newSnakeHeadPos, self.apples)
        if eatenAppleIndex is not None:
            # rem old apple
            del self.apples[eatenAppleIndex]
            self.spawnRndApple()
            self.score += 1
        else:
            self.snake.pos.pop(-1)

        return True