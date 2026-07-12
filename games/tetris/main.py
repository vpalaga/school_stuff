import pygame
from pygame.locals import *
import time
import sys
from colors import Colors

from objects import Pos

from game import Game

class Display:
    def __init__(self):
        self.version = "0.0.2"
        pygame.init()

        # Window title (taskbar / title bar text)
        pygame.display.set_caption("TETRIS")

        # Window icon
        #icon = pygame.image.load(resource_path("images/billeter_icon.png"))
        #pygame.display.set_icon(icon)

        self.fps = 15
        self.fps_p_tick = 4

        self.screen = pygame.display.set_mode(Colors.windowSize)

        self.game = Game()

        self.fpsClock = pygame.time.Clock()

        # setup (do once)
        self.fontNormal = pygame.font.Font(None, 50)  # None = default font, 36 = size
        self.fontSmall = pygame.font.Font(None, 20)  # None = default font, 36 = size
        self.fontBig = pygame.font.Font(None, 80)  # None = default font, 36 = size

    def drawRect(self, pos: Pos, color: tuple[int,int,int], offset:float=1):

        if not self.game.tools.isPosOnScreen(pos):
            return

        pos = self.game.tools.translateCoords(pos)

        rect = (pos.x - (self.game.tools.sField / 2)*offset, pos.y - (self.game.tools.sField / 2)*offset,
                self.game.tools.sField*offset, self.game.tools.sField*offset)

        pygame.draw.rect(self.screen, color, rect)

        offset = .9
        color = self.game.tools.brightenColor(color)

        rect = (pos.x - (self.game.tools.sField / 2)*offset, pos.y - (self.game.tools.sField / 2)*offset,
                self.game.tools.sField*offset, self.game.tools.sField*offset)

        pygame.draw.rect(self.screen, color, rect)

    def drawFieldOutline(self)->None:
        thickness = Pos(Colors.playfieldOutlineThickness, Colors.playfieldOutlineThickness)
        dimension = self.game.tools.gameSizePx + thickness + thickness
        print(dimension)
        leftTop = self.game.tools.zeroPos + -thickness
        rect = (*leftTop.pos, *dimension.pos)
        print(rect)
        pygame.draw.rect(self.screen, Colors.outline, rect)

    def drawField(self)->None:
        for y in range(Colors.gameSize[1]):
            for x in range(Colors.gameSize[0]):
                if (x + y) % 2 == 0:
                    color = Colors.lGray
                else:
                    color = Colors.dGray

                self.drawRect(Pos(x, y), color)

    def drawPlayField(self):
        for field in self.game.playField.values():
            self.drawRect(field.pos, field.color)

    def drawFallingShape(self):
        bs = self.game.fallingShape.blockStruct
        for block in bs.blocks:
            self.drawRect(block, bs.color)

    def text(self)->None:

        surface = self.fontBig.render(str(self.game.score), True, Colors.score)  # text, antialias, color
        rect = surface.get_rect(center=self.game.tools.scorePos.pos)

        self.screen.blit(surface, rect)

    def draw(self):
        self.screen.fill(Colors.background)
        self.drawFieldOutline()
        self.drawField()

        self.drawPlayField()

        self.drawFallingShape()
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
                    if key == pygame.K_DOWN or key == pygame.K_s:
                        return

    def events(self):
        rotation = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                key = event.key

                if key == pygame.K_UP or key == pygame.K_w:
                    rotation = -1
                elif key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # --- outside the event loop, runs every frame, detects held keys ---
        keys = pygame.key.get_pressed()
        move = Pos(0, 0)

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move += Pos(0, 1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move += Pos(1, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move += Pos(-1, 0)

        nextFallingShapeBS = self.game.fallingShape.blockStructByOffsetAndRotation(offset=move, rotation=rotation)

        if self.game.checkBSValidity(nextFallingShapeBS):
            self.game.fallingShape.midPos += move
            self.game.fallingShape.rotate(rotation)

            self.game.fallingShape.updateBS()

    def update(self):
        pygame.display.flip()
        self.fpsClock.tick(self.fps)

if __name__ == "__main__":
    display = Display()
    tickCounter = 0
    # draw init screen
    display.draw()

    while True:
        display.events()
        display.draw()

        if tickCounter == display.fps_p_tick:
            # main tick game logic, False -> gameOver
            if not display.game.updateOnTick():
                print("game over...")
                time.sleep(1)

                # reset for new game
                display.game = Game()
                display.draw()

            tickCounter = 0
        else:
            tickCounter += 1