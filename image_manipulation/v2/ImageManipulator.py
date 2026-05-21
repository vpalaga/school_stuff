import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image

import functools
from typing import Tuple, List, Callable, Any
import os
"""

# 1. Bild aus einer Datei in eine Liste lesen
img_list = mpimg.imread("./bilder/frosch.jpg")
img = img_list.copy().astype(np.uint8)

print(img[0][0]) # Was wird hier ausgegeben?

# TODO: Schreibe ein Schleife, die über jedes Pixel iteriert und diese manipuliert.

img2 = Image.fromarray(img)
img2.save("./cx_out/filtered.jpg")
"""

class Manipulate:
    DEFAULT_PATH = r"bilder/frosch.jpg"
    def __init__(self, image_path=None)->None:
        # use frog if no path is specified...
        self.imagePath = image_path if isinstance(image_path, str) else self.DEFAULT_PATH

        # check if path exists
        if not os.path.exists(self.imagePath):
            raise FileNotFoundError(f"Image not found: {self.imagePath}")

        self.image = mpimg.imread(self.imagePath).copy().astype(np.uint8)

        # store manipulation history into a list (Image, manipulation method: str) as method name
        self.imageHistory: List[tuple[Image.Image, str]] = []

        # image constants:
        self.HEIGHT, self.WIDTH = self.image.shape[:2]
        print(f"width: {self.WIDTH}, height: {self.HEIGHT}")
        self.widthRange  = range(self.WIDTH)
        self.heightRange = range(self.HEIGHT)

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

    # Effects -------------------------------------------------------------
    @save_history
    def default(self) -> Image.Image:
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

if __name__ == "__main__":
    manip = Manipulate()

    manip.invert().show()
    manip.history()


