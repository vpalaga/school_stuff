import sys
import pygame
from pygame.locals import *
import time
import os, sys

from game import Game
from data import Colors, Pos


def resource_path(relative):
    base = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    return os.path.join(base, relative)

class Snake:
    def __init__(self):
        self.width, self.height = 600, 700
        self.colors = Colors()
        self.game = Game(9)

        self.tickHeading = Pos(1,0)
        self.headingDelta = self.game.snake.heading / self.game.fpsPerGametick

        pygame.init()
        self.fpsClock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((self.width, self.height))
        # setup (do once)
        self.fontBig = pygame.font.Font(None, 50)  # None = default font, 36 = size
        self.fontSmall = pygame.font.Font(None, 25)  # None = default font, 36 = size

        # render and draw

        self.appleSprites = self._loadAppleSprites()

        self.midPos = self.game.tools.generateMidposDict()
        self.snakeHead = self._loadHead()



    def _loadHead(self)->pygame.Surface:
        img = pygame.image.load(resource_path("images/Pi7_cropper.png")).convert_alpha()
        img = pygame.transform.scale(img, (self.game.tools.xField * 1.5, self.game.tools.xField*1.5))
        return img

    def _loadAppleSprites(self)->list[pygame.Surface]:
        sprites = []

        directory = resource_path(r"images/apples")
        for filename in os.listdir(directory):
            img = pygame.image.load(os.path.join(directory, filename)).convert_alpha()
            img = pygame.transform.scale(img, (self.game.tools.xField * 1.2, self.game.tools.xField * 1.2))
            sprites.append(img)
        return sprites

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

    def drawSnake(self, tick:int)->None:
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

        headRect = self.snakeHead.get_rect(center=self.game.tools.translateCoords(self.game.snake.headPos).pos)
        self.screen.blit(self.snakeHead, headRect)

    def drawApples(self)->None:
        for pos, spriteIndex in self.game.apples.items():
            #pygame.draw.circle(self.screen, self.colors.apple, pos, self.game.tools.xField*0.7)

            appleRect = self.appleSprites[spriteIndex].get_rect(center=self.midPos[pos].pos)
            self.screen.blit(self.appleSprites[spriteIndex], appleRect)
    def text(self)->None:

        surface = self.fontBig.render(f"SCORE: {self.game.score}", True, (255, 255, 255))  # text, antialias, color
        rect = surface.get_rect(midleft=(30, 50))

        self.screen.blit(surface, rect)

        surface = self.fontSmall.render(f"PRESS RIGHT ARROW TO PLAY", True, (255, 255, 255))  # text, antialias, color
        rect = surface.get_rect(center=(400, 50))

        self.screen.blit(surface, rect)

    def draw(self, tick:int):
        self.screen.fill(self.colors.background)
        self.drawFiled()
        self.drawApples()
        self.drawSnake(tick)
        self.text()

        self.update()
    def waitForRightKey(self):
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
                if -self.game.snake.heading != newHeading:
                    self.tickHeading = newHeading

    def update(self):
        pygame.display.flip()
        self.fpsClock.tick(self.game.fps)

if __name__ == "__main__":
    snake = Snake()
    tickCounter = 0
    displayedScore = -1
    snake.draw(tickCounter)
    snake.waitForRightKey()
    while True:
        if displayedScore != snake.game.score:
            displayedScore = snake.game.score
            print(f"LIVES DESTROYED: {displayedScore}")

        snake.game.snake.headPos += snake.headingDelta
        snake.events()
        snake.draw(tickCounter)
        if tickCounter == snake.game.fpsPerGametick:
            snake.game.snake.heading = snake.tickHeading
            if not snake.game.updateOnTick():
                print("game over...")
                snake.waitForRightKey()
                snake.game = Game(len(snake.appleSprites))
                snake.tickHeading = Pos(1,0)
                snake.draw(tickCounter)
                snake.waitForRightKey()
            snake.headingDelta = snake.game.snake.heading / snake.game.fpsPerGametick
            tickCounter = 0

        else:

            tickCounter += 1