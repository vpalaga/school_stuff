import sys
import pygame
from pygame.locals import *
import time
from bot import Bot

from field_gen import Playground

class Game:
    player_color = ["RED", "BLUE", "GREEN"]

    def __init__(self):
        pygame.init()
        self.won_pos = None
        self.update_final_time = True

        self.fps = 60
        self.fpsClock = pygame.time.Clock()

        #players turns: 0,1
        self.turn = 0

        self.width, self.height = 700, 700
        self.size = (16, 16)
        self.players = 2
        self.bot = Bot()

        self.play = Playground(self.size, (self.width, self.height))
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.my_font = pygame.font.SysFont('Comic Sans MS', round(self.play.yField * 0.5))

    def grid(self):
        for y in range(self.size[1]):
            pygame.draw.line(self.screen, (0, 0, 0), (0, y * self.play.yField), (self.width, y * self.play.yField))

        for x in range(self.size[0]):
            pygame.draw.line(self.screen, (0, 0, 0), (x * self.play.xField, 0), (x * self.play.xField, self.height))

    def draw_eval_map(self, eval_map:dict[tuple[int,int],float])->None:
        for pos, field_eval in self.bot.eval_map.items():
            x_pixel, y_pixel = self.play.mid_pos[pos]

            text = self.my_font.render(str(round(field_eval, 3)), False, (0,0,0))
            text_rect = text.get_rect(center=(x_pixel, y_pixel))
            self.screen.blit(text, text_rect)

    def draw(self)->None:
        self.screen.fill((210, 210, 210))
        self.grid()

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.play.state[(x, y)] is not None:

                    match self.play.state[(x, y)]:
                        case 0:
                            pygame.draw.circle(self.screen, (255,0,0), self.play.mid_pos[x, y], self.play.xField * 0.4)
                        case 1:
                            pygame.draw.circle(self.screen, (0,0,255), self.play.mid_pos[x, y], self.play.xField * 0.4)
                        case 2:
                            pygame.draw.circle(self.screen, (100,200,50), self.play.mid_pos[x, y], self.play.xField * 0.4)

        self.draw_eval_map(self.bot.eval_map)

    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                xr = int(x // self.play.xField)
                yr = int(y // self.play.yField)

                pos = (xr, yr)

                if pygame.mouse.get_pressed()[0]:  # Left click

                    # check is played before
                    if self.play.state[pos] is None:
                        self.play.state[pos] = self.turn
                        print(f"clicked at {pos}")

                        #flip turn
                        self.turn += 1
                        if self.turn == self.players:
                            self.turn = 0
                        print(f"next turn: {Game.player_color[self.turn]}")
                        print("-"*100)

                        # bots turn
                        self.bot.calculate_eval_map(self.play.state)
                        bot_play = self.bot.best_move()
                        self.play.state[bot_play] = self.turn

                        # flip turn
                        self.turn += 1
                        if self.turn == self.players:
                            self.turn = 0

                        print(f"next turn: {Game.player_color[self.turn]}")
                        print("-" * 100)


                        won_pos = self.play.check_for_wins()

                        if won_pos is not None:
                            self.draw()
                            self.handle_win(won_pos)
                            self.update()

                            return True
        return False

    def handle_win(self, start_end)-> None:
        print("s-------------------------")
        print(start_end)
        pygame.draw.line(self.screen, (70,70,70),self.play.mid_pos[start_end[0]], self.play.mid_pos[start_end[1]], width=10)

    def update(self):
        pygame.display.flip()
        self.fpsClock.tick(self.fps)

if __name__ == "__main__":
    game = Game()
    won = False
    while True:

        game.draw()

        if not won and game.events():
            won = True
            time.sleep(2.5)
            pygame.quit()
            sys.exit()

        if not won:
            game.update()
