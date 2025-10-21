from PIL import Image, ImageDraw, ImageFont


def fire_time(f1:tuple[int, int], f2:tuple[int, int]) -> int:
    x1, y1 = f1
    x2, y2 = f2

    distance = abs(x1 - x2) + abs(y1 - y2) - 1
    return round(distance / 2)

def font(size):
    return ImageFont.truetype("arial.ttf", size)

# Create a blank white image

class FireImage:
    def __init__(self, n_, fire_dict_ : dict[int,tuple[int, int]], fire_diagram_, wh=1000):
        self.n = n_
        #self.fire_diagram = fire_diagram_
        self.fire_dict = fire_dict_
        self.side = wh

        self.tile_size = self.side / (self.n + 2)

        self.mid_pos = self.clac_mid_pos()

        self.img = Image.new("RGB", (self.side, self.side), color="white")
        self.draw = ImageDraw.Draw(self.img)

    def make_vis(self):
        self.grid()
        self.plot_fires()
        self.plot_fire_distances()

        self.img.show()
        self.img.save("vis/simple_image.png")

    def plot_fire_distances(self):
        self.plot_start_end_distances()
        self.plot_mid_node_distances()

    def clac_mid_pos(self):
        mid_pos = {}
        x_offset = self.tile_size / 2
        y_offset = self.tile_size / 2

        for x in range(-1, self.n + 1):
            for y in range(-1, self.n + 1):
                mid_pos[(x, y)] = (x_offset + ((x + 1) * self.tile_size), y_offset + ((y + 1) * self.tile_size))

        return mid_pos

    def grid(self):

        tile_size_half = self.tile_size // 2

        for (x_g, y_g), (x, y) in self.mid_pos.items():
            fill = "white"

            if x_g == -1 or x_g == self.n or y_g == -1 or y_g == self.n:
                fill = "grey"

            self.draw.rectangle((x - tile_size_half, y - tile_size_half, x + tile_size_half, y + tile_size_half),
                                outline="black", fill=fill)
            self.draw.text((x, y), f"{x_g}:{y_g}", "darkgrey", )

    def plot_fires(self):
        for fire_nr, (x, y) in self.fire_dict.items():
            pos = self.mid_pos[(x, y)]
            self.draw.circle(pos, self.tile_size / 2 - 5, "orange")
            self.draw.text(pos, str(fire_nr), "black")

    def plot_start_end_distances(self):

        for i, fire in self.fire_dict.items():
            s, e, s_l, e_l = self.dist_from_S_E(*fire)

            self.line(fire, s, "start", ln=s_l)
            self.line(fire, e, "end",   ln=e_l)

    def plot_mid_node_distances(self):
        visited = []
        for i, fire_start in self.fire_dict.items():

            for ii, fire_end in self.fire_dict.items():
                if i != ii and (i, ii) not in visited:
                    self.line(fire_start, fire_end)
                    visited.append((i, ii))
                    visited.append((ii, i))

    def dist_from_S_E(self, x, y):
        """
        Returns the x, y pos to minimal start node and end node
        start, end"""

        if x < self.n - y - 1:
            ret_x = (-1, y)
        else:
            ret_x = (x, self.n)

        if y < self.n - x - 1:
            ret_y = (x, -1)
        else:
            ret_y = (self.n, y)

        return ret_x, ret_y, min(x, self.n - y -1 ), min(y, self.n - x - 1)

    def line(self, start:tuple[int, int], end:tuple[int, int], line_type="basic", ln=None):
        types = {
            "basic": ("black", 3),
            "start": ("green", 3),
            "end":   ("red",   3)
        }
        if line_type not in list(types.keys()):
            line_type = "basic"

        if ln is None:
            ln = fire_time(start, end)

        start_rel, end_rel = self.mid_pos[start], self.mid_pos[end]
        cl, wd = types[line_type]

        self.draw.line((*start_rel,*end_rel), cl, wd)

        mid = ((start_rel[0] + end_rel[0]) / 2,
               (start_rel[1] + end_rel[1]) / 2) # clac the mid pos for the text to go

        self.draw.text(mid, f"{ln}", "darkblue", font=font(50))

FireImage(8,
          {0: (7, 1), 1: (1, 5), 2: (2, 7)},
          {
                -1: {0: 6, 1: 1, 2: 0},
                0: {1: 4, 2: 5, 3: 0},
                1: {0: 4, 2: 1, 3: 5},
                2: {0: 5, 1: 1, 3: 5},
                3: {}}
          ).make_vis()