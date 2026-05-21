import numpy as np
import matplotlib.pyplot as plt

class ImageCreator:
    def __init__(self, size:tuple[int, int])->None:
        self.WIDTH, self.HEIGHT = size
        self.canvas = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)

    def fill(self, color:int|tuple[int,int,int]=0)->None:
        if isinstance(color, int):
            color = (color, color, color)
        self.canvas[:] = color

    def set_pixel(self, pixel:tuple[int,int], color:tuple[int,int,int]|int)->None:
        if isinstance(color, int):
            color = (color, color, color)
        x, y = pixel
        self.canvas[y, x] = color

    def checker_board(self)->None:
        for y in range(self.HEIGHT):
            white = False
            if y % 2 == 0:
                white = True
            for x in range(self.WIDTH):
                if white:
                    self.set_pixel((x, y), 200)
                else:
                    self.set_pixel((x, y), 255)
                white = not white

    def show(self)->None:
        plt.imshow(self.canvas)
        #plt.axis("off")  # optional: hides axes
        plt.show()

    def line(self, start:tuple[int,int], end:tuple[int,int]):
        def bh(step:float|int, lead:int):
            for i in range(lead):
                yield i, round(step * i)

        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if dx > dy:
            s = dy / dx
            for x, y in bh(s, dx):
                self.set_pixel((start[0] + x, start[1] + y), 0)
        else:
            s = dx / dy
            for y, x in bh(s, dy):
                self.set_pixel((start[0] + x, start[1] + y), 0)

    def circle(self, origin:tuple[int,int],radius:int, color:tuple[int,int,int]|int)->None:
        if isinstance(color, int):
            color = (color, color, color)

        # use Pythagorean method of checking
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx**2 + dy**2 <= radius**2:
                    self.set_pixel((origin[0] + dx, origin[1] + dy), color)

    def export(self):
        return self.canvas

if __name__ == "__main__":
    c = ImageCreator((100,100))
    c.checker_board()
    c.circle((50,50), 30, 0)
    c.show()