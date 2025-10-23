from PIL import Image, ImageDraw, ImageFont
import random

from path_alg import Path, fire_time, dist_from_S_E

def font(size):
    return ImageFont.truetype("arial.ttf", size)

class FireImage:
    def __init__(self, n_, fire_dict_ : dict[int,tuple[int, int]], wh=1000):
        self.n = n_
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

        max_w = Path(self.fire_dict, self.n).max_path_weight
        print(f"MAX: {max_w}")
        #self.plot_path(path)

        self.img.show()
        #self.img.save("vis/simple_image.png")

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
            cols = {"white": (255, 255, 255),
                    "l_green": (224, 184, 184),
                    "l_red": (184, 224, 184)}
            fill = "white"

            if x_g == -1 or y_g == self.n:
                fill = "l_red"

            if y_g == -1 or x_g == self.n:
                if fill == "l_red":
                    fill = "white"
                else:
                    fill = "l_green"



            self.draw.rectangle((x - tile_size_half, y - tile_size_half, x + tile_size_half, y + tile_size_half),
                                outline="black", fill=cols[fill])
            self.draw.text((x, y), f"{x_g}:{y_g}", "darkgrey", )

    def plot_fires(self):
        for fire_nr, (x, y) in self.fire_dict.items():
            pos = self.mid_pos[(x, y)]
            self.draw.circle(pos, self.tile_size / 2 - 5, "orange")
            self.draw.text(pos, str(fire_nr), "red", font=font(50))

    def plot_start_end_distances(self):

        for i, fire in self.fire_dict.items():
            s, e, s_l, e_l = dist_from_S_E(*fire, n=n, ret_node_from=True)

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

    def plot_path(self, path):
        for i in range(1, len(path)):
            self.line(self.fire_dict[path[i-1]], self.fire_dict[path[i]], line_type="path")

    def line(self, start:tuple[int, int], end:tuple[int, int], line_type="basic", ln=None):
        types = {
            "basic": ("black", None),
            "start": ("green", None),
            "end":   ("red",   None),
            "path":  ("violet",None)
        }

        if line_type not in list(types.keys()):
            line_type = "basic"

        if ln is None:
            ln = fire_time(start, end)

        start_rel, end_rel = self.mid_pos[start], self.mid_pos[end]
        cl, wd = types[line_type]

        if wd is None: # let width be proportional to line.length
            wd = round((1 / (ln + 1)) * 10)

        self.draw.line((*start_rel,*end_rel), cl, wd)

        mid = ((start_rel[0] + end_rel[0]) / 2,
               (start_rel[1] + end_rel[1]) / 2) # clac the mid pos for the text to go

        self.draw.text(mid, f"{ln}", "darkblue", font=font(wd * 10))

#FireImage(8,
#          {0: (7, 1), 1: (1, 5), 2: (2, 7), 3:(2, 5), 4:(3, 5)},
#          ).make_vis()

#FireImage(7,
#          {0: (4, 3), 1: (2, 0), 2: (3, 6)},
#          ).make_vis()
n= 500
m= 5000
fire_ = {x:(random.randint(0, n-1), random.randint(0, n -1)) for x in range(m)}

FireImage(12,
          {0: (8, 2), 1: (6, 10), 2: (6, 6), 3: (11, 5), 4: (5, 3), 5: (6, 0), 6: (3, 3), 7: (4, 6), 8: (8, 10), 9: (2, 4)},
          ).make_vis()