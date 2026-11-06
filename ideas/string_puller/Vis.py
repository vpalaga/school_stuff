import math

from PIL import Image, ImageDraw, ImageFont

from Vector import Vec2

class Img:
    def __init__(self):
        self.objects = []

        self.window_size = Vec2(1000,1000)
        self.integers_in_image:int = 0
        self.pix_p_int:float = 0

        self.font = ImageFont.truetype(r"C:\Windows\Fonts\Arial.ttf", 40)

        self.img: Image.Image = Image.new("RGB", self.window_size.xy, color="white")
        self.draw: ImageDraw.ImageDraw = ImageDraw.Draw(self.img)

    def add_object(self, o)->None:
        self.objects.append(o)

    def _size_of_picture(self)->Vec2:
        mx, my = 0,0
        for obj in self.objects:
            if isinstance(obj, Vec2):
                if abs(obj.x) > mx:
                    mx = abs(obj.x)
                if abs(obj.y) > my:
                    my = abs(obj.y)

        return Vec2(mx,my) * 2

    def calc_pix_per_integer(self):
        size = self._size_of_picture()
        integers_scale = math.ceil(max(size.x, size.y) * 1.5)
        self.integers_in_image = integers_scale
        print(integers_scale)

        self.pix_p_int = self.window_size.x / integers_scale
        self.font = ImageFont.truetype(r"C:\Windows\Fonts\Arial.ttf", min(round(self.pix_p_int*0.5), 40))

    def _translate(self, c:Vec2)->Vec2:
        half_size = self.window_size * 0.5
        scaled = (c * Vec2(1,-1)) * self.pix_p_int + half_size
        return scaled

    def line(self, start:Vec2, end:Vec2, c, w)->None:
        self.draw.line(
            (*self._translate(start).xy,
                *self._translate(end).xy), fill=c, width=w)

    def vector(self, start:Vec2, vec:Vec2)->None:
        print(vec)
        beta = 30
        arrow_len_prc = 0.1

        self.line(start, start+vec, "red", w=4)
        vec_angle = math.degrees(math.atan(vec.x/vec.y))
        arr_len = vec.len() * arrow_len_prc

        top = -Vec2(
            arr_len * math.sin(math.radians(vec_angle + beta)),
            arr_len * math.cos(math.radians(vec_angle + beta))
        )
        bottom = -Vec2(
            arr_len * math.sin(math.radians(vec_angle - beta)),
            arr_len * math.cos(math.radians(vec_angle - beta))
        )

        self.line(start + vec, start + vec + bottom, c="red", w=4)
        self.line(start + vec, start + vec + top, c="red", w=4)

    def axis(self):
        half_vec = self.window_size * 0.5
        print(half_vec)
        self.draw.line((half_vec.x, 0, half_vec.x, self.window_size.y),fill="black", width=3)
        self.draw.line((0, half_vec.y, self.window_size.x, half_vec.y),fill="black", width=3)

        self.calc_pix_per_integer()

        half_integer_range = math.floor(self.integers_in_image / 2)

        for i in range(-half_integer_range, half_integer_range + 1):
            xy = self._translate(Vec2(i,0))
            self.draw.line((xy.x, 0, xy.x, self.window_size.y), fill="gray")

            if i != 0:
                self.draw.text(xy.xy, str(i), fill="black", font=self.font, anchor="ma")

            xy = self._translate(Vec2(0,i))
            self.draw.line((0, xy.y, self.window_size.x, xy.y), fill="gray")

            if i != 0:
                self.draw.text(xy.xy, " "  + str(i), fill="black", font=self.font, anchor="lm")
            else:
                self.draw.text(xy.xy, " "  + str(i), fill="black", font=self.font, anchor="la")

    def create(self):
        self.axis()
        for o in self.objects:
            if isinstance(o, Vec2):
                self.vector(Vec2(0,0), o)
        self.img.show()


