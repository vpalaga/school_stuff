from data import Pos, Snake, Tools
class Game:
    def __init__(self):
        self.gameSize = (20, 20)
        self.applesOnScreen = 3
        self.fpsPerGametick = 60
        self.fps = 60

        self.score = 0

        self.tools = Tools(self.gameSize)
        self.snake = Snake(self.gameSize)
        self.apples: list[Pos] = []
        for _ in range(self.applesOnScreen): self.spawnRndApple()

    def spawnRndApple(self)->None:
        while True:
            apple = self.tools.randomPos()

            if apple in self.apples: continue
            elif apple in self.snake.pos: continue
            else:
                self.apples.append(apple)
                return

    def updateOnTick(self)->bool:
        """True all good, False: gameOver"""
        # clac new head pos
        newSnakeHeadPos = self.snake.headPos + self.snake.heading
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
        if newSnakeHeadPos in self.apples:
            # rem old apple
            self.apples.remove(newSnakeHeadPos)
            self.spawnRndApple()
            self.score += 1
        else:
            self.snake.pos.pop(-1)

        return True