import random

class Playground:
    def __init__(self, size: tuple[int,int], mines:int, pixels:tuple[int,int]):
        self.size = size
        self.mines = mines
        self.xField, self.yField = pixels[0] / size[0], pixels[1] / size[1]

        self.fields = size[0]*size[1]
        self.mine_p_field = (mines / self.fields) * 100 

        self.mine_p_field = 13

        self.playground = {}
        self.mid_pos = {}
        self.state = {}
        self.flags = set()

        self.gen_midpos()

        self.populate_state()
    
    def nulls_around(self, x, y) ->set[tuple[int, int]]:
        nulls = set()

        for dy in range(-1,2):
            for dx in range(-1,2):
                
                if not (dx == 0 and dy == 0):
                    
                    n_x = x+dx
                    n_y = y+dy

                    if 0 <= n_x < self.size[0] and 0 <= n_y < self.size[1]:
                        self.state[(n_x,n_y)] = True

                        if self.playground[(n_x, n_y)] == 0:
                            nulls.add((n_x,n_y))
        return nulls
    
    def clear_null(self, x_start:int, y_start:int):
        cleared = set()
        check = set()

        check.add((x_start, y_start))

        while len(check) > 0:
            x, y = check.pop()

            cleared.add((x, y))
            self.state[(x, y)] = True

            for pos in self.nulls_around(x, y):
                if pos not in cleared: 
                    check.add(pos)



    def populate_state(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.state[(x, y)] = False

    def gen_midpos(self):
        nx = self.xField / 2
        ny = self.yField / 2

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.mid_pos[(x, y)] = (nx,ny)
                nx += self.xField
            nx = self.xField / 2
            ny += self.yField
    
    def generate_mines(self, x_cen:int, y_cen:int):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if random.randint(0,100) <= self.mine_p_field:
                    self.playground[(x, y)] = "m"
     
        for dy in range(-1,2):
            for dx in range(-1,2):
                if (x_cen + dx, y_cen + dy) in self.playground.keys():
                    del self.playground[(x_cen + dx, y_cen + dy)]


    def mines_around_pos(self, x:int, y:int) -> int:
        count = 0

        for dy in range(-1,2):
            for dx in range(-1,2):
                
                if not (dx == 0 and dy == 0):
                    n_x = x+dx
                    n_y = y+dy

                    if (n_x, n_y) in self.playground.keys():
                        if self.playground[(n_x,n_y)] == "m":
                            count += 1
        return count

    def generate_rest(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if (x, y) not in self.playground.keys():
                    # set the count around, x,y
                    self.playground[(x, y)] = self.mines_around_pos(x, y)

    def show(self):
        for y in range(self.size[1]):
            line = ""
            for x in range(self.size[0]):
                line += "| " + (str(self.playground[(x, y)] if self.playground[(x, y)] != 0 else " " )) + " "
            line += "|"
            print(line)
