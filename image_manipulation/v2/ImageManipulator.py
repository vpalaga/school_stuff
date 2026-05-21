import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

import functools
from typing import Tuple, List, Callable, Any
import os

from ImageCreator import ImageCreator

class Manipulate:
    class Tools:
        BLACK = 0,0,0
        WHITE = 255,255,255
        @staticmethod
        def black_white(color: tuple[int,...])->float|int:
            """return average color 0-1"""
            return (sum(color)) / (len(color) * 255)

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
    def binary(self, t:float|int)->Image.Image:
        """t: threshold"""
        new_image = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)

        for y in self.heightRange:
            for x in self.widthRange:
                if Manipulate.Tools.black_white(self.image[y, x]) < t:
                    new_image[y, x] = Manipulate.Tools.BLACK
                else:
                    new_image[y, x] = Manipulate.Tools.WHITE

        self.image = new_image
        return Image.fromarray(new_image)

    @save_history
    def edge_detection_v1(self, radius:int)->Image.Image:
        """draw red pixels into edges"""

        def check_around(x:int, y:int)->bool:
            for dy in range(0,radius+1):
                for dx in range(0,radius+1):
                    if dy == dx == 0:
                        continue



        for y in self.heightRange:
            for x in self.widthRange:




if __name__ == "__main__":
    c = ImageCreator((100,100))
    c.fill(255)
    c.circle((50,50), 30, 0)
    manip = Manipulate(image=c.export())

    manip.history()
    manip.show()
