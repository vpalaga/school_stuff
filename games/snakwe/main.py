import pygame
from pygame.locals import *
import time
import sys

from game import Game
from data import Colors, Pos, resource_path

class Snake:
    def __init__(self):
        self.version = "1.1.1"
        pygame.init()

        # Window title (taskbar / title bar text)
        pygame.display.set_caption("1 Dih-stroyer")

        # Window icon
        icon = pygame.image.load(resource_path("images/billeter_icon.png"))
        pygame.display.set_icon(icon)

        self.width, self.height = 600, 700
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.colors = Colors()
        self.game = Game()

        # buffer with next moves allows for pre-moves
        self.tickHeading = []
        self.headingDelta = self.game.snake.heading / self.game.fpsPerGametick

        self.fpsClock = pygame.time.Clock()

        # setup (do once)
        self.fontNormal = pygame.font.Font(None, 50)  # None = default font, 36 = size
        self.fontSmall = pygame.font.Font(None, 20)  # None = default font, 36 = size
        self.fontBig = pygame.font.Font(None, 80)  # None = default font, 36 = size

        self.midPos = self.game.tools.generateMidposDict()

    def drawRect(self, pos: Pos, color: tuple[int,int,int], offset:float=1):

        pos = self.game.tools.translateCoords(pos)

        rect = (pos.x - (self.game.tools.xField / 2)*offset, pos.y - (self.game.tools.yField / 2)*offset,
                self.game.tools.xField*offset, self.game.tools.yField*offset)
        pygame.draw.rect(self.screen, color, rect)

    def drawFiled(self)->None:
        for y in range(self.game.gameSize[1]):
            for x in range(self.game.gameSize[0]):
                if (x + y) % 2 == 0:
                    color = self.colors.lightGrass
                else:
                    color = self.colors.darkGrass
                self.drawRect(Pos(x, y), color)

    def drawSnake(self)->None:
        w = .9
        for i in range(len(self.game.snake.pos)):
            pos = self.game.snake.pos[i]
            self.drawRect(pos, self.colors.snake, max(w, .6))
            if i != len(self.game.snake.pos) - 1:
                nextPos = self.game.snake.pos[i+1]
                midPos = Pos(((pos.x + nextPos.x) / 2), (pos.y + nextPos.y)/2)
                self.drawRect(midPos, self.colors.snake, max(w, .6))
            w -= .03

        self.drawRect(self.game.snake.headPos, self.colors.snake, 1.1)

        headRect = self.game.snake.img.get_rect(center=self.game.tools.translateCoords(self.game.snake.headPos).pos)
        self.screen.blit(self.game.snake.img, headRect)

    def drawApples(self)->None:
        for apple in self.game.apples:
            #pygame.draw.circle(self.screen, self.colors.apple, pos, self.game.tools.xField*0.7)

            appleRect = apple.img.get_rect(center=self.midPos[apple.pos.pos].pos)
            self.screen.blit(apple.img, appleRect)

    def text(self)->None:

        surface = self.fontNormal.render(f"SCORE: {self.game.score}", True, (255, 255, 255))  # text, antialias, color
        rect = surface.get_rect(midleft=(30, 40))

        self.screen.blit(surface, rect)

        surface = self.fontSmall.render(f"PRESS RIGHT ARROW TO PLAY", True, (255, 255, 255))  # text, antialias, color
        rect = surface.get_rect(midleft=(10, 80))

        self.screen.blit(surface, rect)

        surface = self.fontBig.render(f"1 DIH-stroyer", True, self.colors.title)  # text, antialias, color
        rect = surface.get_rect(center=(400, 50))

        self.screen.blit(surface, rect)


    def draw(self):
        self.screen.fill(self.colors.background)
        self.drawFiled()
        self.drawApples()
        self.drawSnake()
        self.text()

        self.update()

    @staticmethod
    def waitForRightKey():
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_RIGHT:
                        return

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                key = event.key
                newHeading = self.game.snake.heading
                if key == pygame.K_UP:
                    newHeading = Pos(0, -1)
                elif key == pygame.K_DOWN:
                    newHeading = Pos(0, 1)
                elif key == pygame.K_RIGHT:
                    newHeading = Pos(1, 0)
                elif key == pygame.K_LEFT:
                    newHeading = Pos(-1, 0)

                # check against backwards movement
                if len(self.tickHeading) > 0:
                    if -self.tickHeading[-1] != newHeading:
                        self.tickHeading.append(newHeading)
                else:
                    if -self.game.snake.heading != newHeading:
                        self.tickHeading.append(newHeading)

    def update(self):
        pygame.display.flip()
        self.fpsClock.tick(self.game.fps)

if __name__ == "__main__":
    snake = Snake()
    tickCounter = 0
    # draw init screen
    snake.draw()
    snake.waitForRightKey()

    while True:
        # update head by small amt for smooth animation
        snake.game.snake.headPos += snake.headingDelta

        snake.events()
        snake.draw()

        if tickCounter == snake.game.fpsPerGametick:



            # if any heading changes are pending, apply these
            if len(snake.tickHeading) > 0:

                # if more than 2 heading changes are set to happen, let only the 2 first ones go through
                if len(snake.tickHeading) > 2:
                    snake.tickHeading = snake.tickHeading[0:2]

                snake.game.snake.heading = snake.tickHeading.pop(0)
                snake.headingDelta = snake.game.snake.heading / snake.game.fpsPerGametick

            # main tick game logic, False -> gameOver
            if not snake.game.updateOnTick():
                print("game over...")
                time.sleep(1)

                # reset for new game
                snake.game = Game()
                snake.tickHeading = []
                snake.headingDelta = snake.game.snake.heading / snake.game.fpsPerGametick
                snake.draw()

                snake.waitForRightKey()

            tickCounter = 0
        else:
            tickCounter += 1