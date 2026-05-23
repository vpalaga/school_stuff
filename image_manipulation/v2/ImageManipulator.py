import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

import functools
from typing import Tuple, List, Callable, Any
import os
from tqdm import tqdm

import main
from ImageCreator import ImageCreator

class Manipulate:
    class Tools:
        BLACK = 0,0,0
        WHITE = 255,255,255
        RED = 255,0,0
        @staticmethod
        def black_white(color: tuple[int,...])->float|int:
            return np.sum(color, dtype=np.float64) / len(color)
        @staticmethod
        def is_same(p1: float|int, p2: float|int, threshold:float|int):
            if abs(p1-p2) <= threshold:
                return True
            return False

        def __init__(self, width, height)->None:
            self.width = width
            self.height = height

        def is_real_pos(self, x:int, y:int)->bool:
            if 0<=x<self.width and 0<=y<self.height:
                return True
            return False

    DEFAULT_PATH = r"bilder/frosch.jpg"
    def __init__(self, image_path=None, image:None|np.ndarray=None)->None:

        # use frog if no path is specified...
        self.imagePath = image_path if isinstance(image_path, str) else self.DEFAULT_PATH

        # check if path exists
        if not os.path.exists(self.imagePath):
            raise FileNotFoundError(f"Image not found: {self.imagePath}")

        self.image = mpimg.imread(self.imagePath).copy().astype(np.uint8)

        if image is not None:
            self.image = image

        # store manipulation history into a list (Image, manipulation method: str) as method name
        self.imageHistory: List[tuple[Image.Image, str]] = []

        # image constants:
        self.HEIGHT, self.WIDTH = self.image.shape[:2]
        print(f"width: {self.WIDTH}, height: {self.HEIGHT}")
        self.widthRange  = range(self.WIDTH)
        self.heightRange = range(self.HEIGHT)

        self.tools = Manipulate.Tools(width=self.WIDTH, height=self.HEIGHT)

    @staticmethod
    def save_history(func: Callable[..., Any])->Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            # save current state after modification
            result = func(self, *args, **kwargs)
            self.imageHistory.append((self.image.copy(), func.__name__))
            return result

        return wrapper

    def history(self):
        """show the contents of Manipulate.imageHistory: image, manipulation method"""
        print("__History__:")
        for img, manipulationMethod in self.imageHistory:
            print(f"{manipulationMethod}: IMG") # leave for now (find better way of showing multiple images at once)

    def show(self):
        title = "default" if len(self.imageHistory) == 0 else self.imageHistory[-1][1]
        plt.title(title) # last manipulation name
        plt.imshow(self.image)
        plt.show()

    # Effects -------------------------------------------------------------
    @save_history
    def default(self) -> Image.Image:
        return Image.fromarray(self.image)

    # don't use as the constants won't get updated
    @save_history
    def _set_image(self, set_to: np.ndarray)->Image.Image:
        self.image = set_to
        return Image.fromarray(self.image)

    @save_history
    def invert(self)-> Image.Image:
        new_image = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)

        for y in self.heightRange:
            for x in self.widthRange:
                pixel = self.image[y, x]
                new_image[y, x] = (255 - pixel[0], 255 - pixel[1], 255 - pixel[2])

        # update image
        self.image = new_image
        return Image.fromarray(new_image)

    @save_history
    def binary(self, t:float|int)->np.ndarray:
        """t: threshold"""
        new_image = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)

        for y in self.heightRange:
            for x in self.widthRange:
                if Manipulate.Tools.black_white(self.image[y, x]) < t:
                    new_image[y, x] = Manipulate.Tools.BLACK
                else:
                    new_image[y, x] = Manipulate.Tools.WHITE

        #self.image = new_image
        return new_image

    @save_history
    def edge_detection_v1(self, threshold:float|int=.2, radius:int=1, noise_min:float|int=2, noise_max:float|int=6)->np.ndarray:
        """draw red pixels into edges, noize n * radius ** 2 """
        edge_mask = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)

        sourceImageArray = self.binary(0.3)

        edge_noise_min = pow(radius, 2) * noise_min
        edge_noise_max = pow(radius, 2) * noise_max

        def is_edge(_x:int, _y:int)->bool:
            originPixelValue: float|int = Manipulate.Tools.black_white(sourceImageArray[_y, _x])
            edge_detected_count = 0

            for dy in range(-radius,radius+1):
                for dx in range(-radius,radius+1):
                    if dy == dx == 0:
                        continue
                    x = _x + dx
                    y = _y + dy

                    if not self.tools.is_real_pos(x, y):
                        continue

                    pixelValue = Manipulate.Tools.black_white(sourceImageArray[y, x])

                    # check if field is defined as different with a threshold
                    if not Manipulate.Tools.is_same(originPixelValue, pixelValue, threshold):
                        # trigger positive return if is triggered multiple times
                        edge_detected_count += 1

            if edge_noise_min < edge_detected_count < edge_noise_max:
                return True
            return False

        bar = tqdm(total=self.HEIGHT * self.WIDTH)

        for y in self.heightRange:
            for x in self.widthRange:
                if is_edge(x, y):
                    edge_mask[y, x] = Manipulate.Tools.RED

            bar.update(self.WIDTH)

        return edge_mask
    @save_history
    def blur(self, radius:int=3)->np.ndarray:
        bluredImageArray = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)

        def avg_color(_x:int, _y:int)->tuple[int,int,int]:
            """return avg color of sector round xy (black and white)"""
            color = 0
            fields = ((radius*2)**2)
            for dy in range(-radius,radius+1):
                for dx in range(-radius,radius+1):
                    if dy == dx == 0:
                        continue
                    x = _x + dx
                    y = _y + dy
                    if not self.tools.is_real_pos(x, y):
                        continue

                    color += self.tools.black_white(self.image[y, x])

            avgColor = round(color / ((radius*2 + 1)**2))
            return avgColor, avgColor, avgColor

        print("blur-ing...")
        bar = tqdm(total=self.HEIGHT * self.WIDTH)

        for y in self.heightRange:
            for x in self.widthRange:
                bluredImageArray[y, x] = avg_color(y, x)
            bar.update(self.WIDTH)

        return bluredImageArray

if __name__ == "__main__":
    c = ImageCreator((100,100))
    c.fill(255)
    c.circle((50,50), 30, 0)
    manip = Manipulate(image=c.export())

    t = .2
    r = 1
    nmn = 2
    nmx = 6

    #v1_array = manip.edge_detection_v1(threshold=t, radius=r, noise_min=nmn, noise_max=nmx)
    plt.imshow(c.export())
    plt.show()
    plt.imshow(manip.blur())
    #plt.title(f"t={t} r={r} n={nmn}:{nmx}")
    plt.show()

    manip.history()
    #manip.show()
