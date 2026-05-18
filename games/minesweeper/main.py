import sys
import pygame
from pygame.locals import *
from playground_gen import Playground
from imgs.wins import open_w
import random

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

        self.width, self.height = 600, 600
        self.x_shift, self.y_shift = 0, 0
        self.window_fields = (15, 15)
        self.size = (15, 15)

        self.play = Playground(self.size, 3, (self.width,self.height), self.window_fields)

        self.screen = pygame.display.set_mode((self.width, self.height))

        self.my_font = pygame.font.SysFont('Comic Sans MS', round(self.play.yField))


    def grid(self):
        for y in range(self.size[1]):
            pygame.draw.line(self.screen,(0,0,0),(0, y*self.play.yField),(self.width, y*self.play.yField))

        for x in range(self.size[0]):
            pygame.draw.line(self.screen, (0,0,0),(x*self.play.xField,0),(x*self.play.xField, self.height))
    
    def dr_flags(self):
        for (xr, yr) in self.play.flags:
            xr = self.x_shift + xr
            yr = self.y_shift + yr

            x, y = self.play.mid_pos[(xr, yr)]

            pygame.draw.line(self.screen, (0,255,0),(x - (self.play.xField / 2), y - (self.play.yField / 2)), (x + (self.play.xField / 2), y + (self.play.yField / 2)), width=round(self.play.xField*.1))
            pygame.draw.line(self.screen, (0,255,0),(x - (self.play.xField / 2), y + (self.play.yField / 2)), (x + (self.play.xField / 2), y - (self.play.yField / 2)), width=round(self.play.xField*.1))

    def dr_field(self, x, y, screen_x, screen_y):
        field = self.play.playground[(x, y)]
        xm, ym = self.play.mid_pos[(screen_x, screen_y)]

        if field == "m":
            pygame.draw.circle(self.screen,(255,0,0),self.play.mid_pos[(screen_x, screen_y)],(self.play.xField / 2) * 0.7)    

            mine = pygame.image.load(r'C:\Users\vit\OneDrive\Documents\GitHub\school_stuff\games\minesweeper\imgs\6250937.jpg').convert_alpha()
            mine = pygame.transform.scale(mine, (self.play.xField, self.play.yField))
            mine_rect = mine.get_rect(center=(xm, ym))

            self.screen.blit(mine, mine_rect)

        elif field == 0:

            pygame.draw.rect(
                self.screen, 
                (210,210,210), 
                (xm - (self.play.xField / 2), 
                 ym - (self.play.yField / 2), 
                 self.play.xField, 
                 self.play.yField))    

        else: 
            pygame.draw.rect(self.screen, (230,230,230), (xm - (self.play.xField / 2), ym - (self.play.yField / 2), self.play.xField, self.play.yField))    

        

            text = self.my_font.render(str(field), False, Game.minesweeper_colors[field])
            text_rect = text.get_rect(center=(xm, ym))
            self.screen.blit(text, text_rect)
    

    
    def draw(self):
        self.screen.fill((255, 255, 255))

        for y in range(self.window_fields[1]):
            for x in range(self.window_fields[0]):

                pos = (x + self.x_shift, y + self.y_shift)
                
                if self.play.state[pos]: # open
                    self.dr_field(*pos,screen_x=x, screen_y=y)
        
        self.dr_flags()
        self.grid()


    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                xr = int(x // self.play.xField) + self.x_shift
                yr = int(y // self.play.yField) + self.y_shift

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
            
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_UP:
                    self.y_shift -= 1
                elif key == pygame.K_DOWN:
                    self.y_shift += 1
                elif key == pygame.K_RIGHT:
                    self.x_shift += 1
                elif key == pygame.K_LEFT:
                    self.x_shift -= 1
                elif key == 1073741911:
                    self.window_fields = (self.window_fields[0] + 1, self.window_fields[1] + 1)

                    self.play.window_fields = self.window_fields

                    self.play.update_field_pixel_size()
                    self.my_font = pygame.font.SysFont('Comic Sans MS', round(self.play.yField))
                    
                elif key == 1073741910:
                    self.window_fields = (self.window_fields[0] - 1, self.window_fields[1] - 1)

                    self.play.window_fields = self.window_fields

                    self.play.update_field_pixel_size()
                    self.my_font = pygame.font.SysFont('Comic Sans MS', round(self.play.yField))
                    
                print(key)        
                self.x_shift = min(max(0, self.x_shift), self.size[0] - self.window_fields[0]) # sqish posible 
                self.y_shift = min(max(0, self.y_shift), self.size[1] - self.window_fields[1]) # sqish posible 
                
    def update(self):
        pygame.display.flip()
        self.fpsClock.tick(self.fps)

    def handle_bomb(self):
        sys.exit()
    
if __name__ == "__main__":
    game = Game()
    while True:
        game.draw()
        game.events()
        game.update()