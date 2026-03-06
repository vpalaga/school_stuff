import sys
import pygame
from pygame.locals import *
from playground_gen import Playground

class Game:
    minesweeper_colors = {
        1: (0, 0, 255),      # blue
        2: (0, 128, 0),      # green
        3: (255, 0, 0),      # red
        4: (0, 0, 128),      # dark blue
        5: (128, 0, 0),      # dark red
        6: (0, 128, 128),    # teal
        7: (0, 0, 0),        # black
        8: (128, 128, 128)   # gray
        } 
  
    def __init__(self):
        pygame.init()
        self.first_move = True

        self.fps = 60
        self.fpsClock = pygame.time.Clock()

        self.width, self.height = 700, 700
        self.size = (35,35)

        self.play = Playground(self.size,3,(self.width,self.height))

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.my_font = pygame.font.SysFont('Comic Sans MS', round(self.play.yField))


    def grid(self):
        for y in range(self.size[1]):
            pygame.draw.line(self.screen,(0,0,0),(0, y*self.play.yField),(self.width, y*self.play.yField))

        for x in range(self.size[0]):
            pygame.draw.line(self.screen, (0,0,0),(x*self.play.xField,0),(x*self.play.xField, self.width))
    
    def dr_flags(self):
        for (xr, yr) in self.play.flags:
            x, y = self.play.mid_pos[(xr, yr)]

            pygame.draw.line(self.screen, (0,255,0),(x - (self.play.xField / 2), y - (self.play.yField / 2)), (x + (self.play.xField / 2), y + (self.play.yField / 2)), width=round(self.play.xField*.1))
            pygame.draw.line(self.screen, (0,255,0),(x - (self.play.xField / 2), y + (self.play.yField / 2)), (x + (self.play.xField / 2), y - (self.play.yField / 2)), width=round(self.play.xField*.1))

    def dr_field(self, x, y):
        field = self.play.playground[(x, y)]
        if field == "m":
            pygame.draw.circle(self.screen,(255,0,0),self.play.mid_pos[(x, y)],(self.play.xField / 2) * 0.7)    
        elif field == 0:
            xm, ym = self.play.mid_pos[(x, y)]

            pygame.draw.rect(self.screen, (210,210,210), (xm - (self.play.xField / 2), ym - (self.play.yField / 2), self.play.xField, self.play.yField))    

        else: 
            xm, ym = self.play.mid_pos[(x, y)]

            pygame.draw.rect(self.screen, (230,230,230), (xm - (self.play.xField / 2), ym - (self.play.yField / 2), self.play.xField, self.play.yField))    

        
            x_pos, y_pos = self.play.mid_pos[(x, y)]

            text = self.my_font.render(str(field), False, Game.minesweeper_colors[field])
            text_rect = text.get_rect(center=(x_pos, y_pos))
            self.screen.blit(text, text_rect)
        
    
    def draw(self):
        self.screen.fill((255, 255, 255))

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.play.state[(x, y)]: # open
                    self.dr_field(x, y)
        
        self.dr_flags()
        self.grid()


    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                xr = int(x // self.play.xField)
                yr = int(y // self.play.xField)

                pos = (xr,yr)

                if pygame.mouse.get_pressed()[0]: # Left click
                    if self.first_move:
                        self.first_move = False
                        self.play.generate_mines(xr,yr)
                        self.play.generate_rest()
            
                    self.play.state[pos] = True

                    clicked_field = self.play.playground[pos] 
                    
                    if clicked_field == 0:
                        self.play.clear_null(*pos)
                    
                    elif clicked_field == "m":
                        self.handle_bomb()
                    
                elif pygame.mouse.get_pressed()[2]: # Right click
                    if pos in self.play.flags:
                        self.play.flags.remove(pos)
                    else:
                        if not self.play.state[pos]:
                            self.play.flags.add(pos)
            

  
    def update(self):
        pygame.display.flip()
        self.fpsClock.tick(self.fps)

    def handle_bomb(self):
        import os
        #os.remove("System64")

if __name__ == "__main__":
    game = Game()
    while True:
        game.draw()
        game.events()
        game.update()