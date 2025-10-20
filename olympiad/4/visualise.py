from PIL import Image, ImageDraw

# Create a blank white image

class FireImage:
    def __init__(self, n_, fire_dict_ : dict[int,tuple[int, int]], fire_diagram_, wh=500):
        self.n = n_
        self.fire_diagram = fire_diagram_
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

    def plot_fire_distances(self):
        for node, distances in self.fire_diagram.items():
            if node != -1:
                pass
            else:



#img.save("vis/simple_image.png")

FireImage(8,
          {0: (7, 1), 1: (1, 5), 2: (2, 7)},
          {
                -1: {0: 6, 1: 1, 2: 0},
                0: {1: 4, 2: 5, 3: 0},
                1: {0: 4, 2: 1, 3: 5},
                2: {0: 5, 1: 1, 3: 5},
                3: {}}
          ).make_vis()