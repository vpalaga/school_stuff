import random

class Playground:
    def __init__(self, size: tuple[int,int], mines:int):
        self.size = size
        self.mines = mines

        self.fields = size[0]*size[1]
        self.mine_p_field = (mines / self.fields) * 100 

        self.playground = {}
    
    def generate_mines(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if random.randint(0,100) <= self.mine_p_field:
                    self.playground[(x, y)] = "m"

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


p = Playground((500, 2), 25)

p.generate_mines()
p.generate_rest()
p.show()
