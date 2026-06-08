import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from typing import List

class Image:
    DEFAULT_IMAGE_PATH = r"bilder/frosch.jpg"
    def __init__(self, imagePath:None|str=None, imageData:None|ndarray=None):
        if imageData is None:
            self.imagePath = imagePath if isinstance(imagePath, str) else self.DEFAULT_IMAGE_PATH
            self.image = self.load(self.imagePath)
        else:
            self.image = imageData
        #save original image for later mapping
        self.originalImage = self.image

        self.HEIGHT, self.WIDTH = self.image.shape[:2]


    @staticmethod
    def load(path: str) -> ndarray:
        """load image as u_int8 ndarray[3]"""

        # check if the image exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")

        img = mpimg.imread(path)
        if img.dtype in (np.float32, np.float64):
            img = (img * 255).astype(np.uint8)
        else:
            img = img.astype(np.uint8)
        return img

    def colorDerivation(self,  threshold: int|float = 50.0)->ndarray:
        img_f = self.image
        grad_mag = np.zeros(img_f.shape[:2])

        for c in range(3):
            gy, gx = np.gradient(img_f[:, :, c])
            grad_mag += gx ** 2 + gy ** 2

        grad_mag = np.sqrt(grad_mag)

        # tune this to your data

        mask = grad_mag > threshold  # boolean array [y, x]
        ys, xs = np.where(mask)  # arrays of y and x coords
        coords = np.column_stack([ys, xs])  # shape [N, 2] — each row is [y, x]

        return coords

    def brightnessAdjust(self, setOff:float|int)->None:
        """offset each pixel of self.image by setOff"""
        setOff = np.array([setOff, setOff, setOff])  # R, G, B offsets
        self.image = np.clip(self.image+setOff,0,255)

    def _fixEdgesAfterBlur(self, image: np.ndarray, radius: int) -> np.ndarray:
        # left edge
        for y in range(radius, self.HEIGHT - radius):
            for x in range(radius):
                image[y, x] = image[y, radius]

        # right edge
        for y in range(radius, self.HEIGHT - radius):
            for x in range(self.WIDTH - radius, self.WIDTH):
                image[y, x] = image[y, self.WIDTH - radius - 1]

        # top edge
        for y in range(radius):
            for x in range(self.WIDTH):
                image[y, x] = image[radius, x]

        # bottom edge
        for y in range(self.HEIGHT - radius, self.HEIGHT):
            for x in range(self.WIDTH):
                image[y, x] = image[self.HEIGHT - radius - 1, x]

        # corners (optional but recommended)
        for y in range(radius):
            for x in range(radius):
                image[y, x] = image[radius, radius]  # top-left

            for x in range(self.WIDTH - radius, self.WIDTH):
                image[y, x] = image[radius, self.WIDTH - radius - 1]  # top-right

        for y in range(self.HEIGHT - radius, self.HEIGHT):
            for x in range(radius):
                image[y, x] = image[self.HEIGHT - radius - 1, radius]  # bottom-left

            for x in range(self.WIDTH - radius, self.WIDTH):
                image[y, x] = image[self.HEIGHT - radius - 1, self.WIDTH - radius - 1]  # bottom-right

        return image
    def blur(self, radius:int=3)->np.ndarray:
        def is_real_pos(_x:int, _y:int)->bool:
            if 0<=_x<self.WIDTH and 0<=_y<self.HEIGHT:
                return True
            return False

        blurredImageArray = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)

        def avg_color(_x:int, _y:int)->tuple[int, ...]:
            """return avg color of sector round xy (black and white)"""
            color = [0,0,0]
            fields = ((radius*2 + 1)**2)
            for dy in range(-radius,radius+1):
                for dx in range(-radius,radius+1):
                    if dy == dx == 0:
                        continue
                    x = _x + dx
                    y = _y + dy
                    if not is_real_pos(x, y):
                        continue

                    field = self.image[y, x]
                    color[0] += int(field[0])
                    color[1] += int(field[1])
                    color[2] += int(field[2])

            avgColor: list[int] = [0,0,0]

            # rgb blur
            avgColor[0] = round(color[0] / fields)
            avgColor[1] = round(color[1] / fields)
            avgColor[2] = round(color[2] / fields)

            return tuple(avgColor)

        print("blur-ing...")

        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                blurredImageArray[y, x] = avg_color(x, y)

        return self._fixEdgesAfterBlur(blurredImageArray, radius)

    def drawArray(self, b:ndarray)->None:
        self.image[b[:, 0], b[:, 1]] = (255,0,0)

    def edgeDetection(self, t:int, r:int)->ndarray:
        self.blur(r)
        coords = self.colorDerivation(threshold=t)
        self.brightnessAdjust(-40)
        self.drawArray(coords)
        return self.image

if __name__ == "__main__":
    i = Image(r"bilder/500by500.jpg")
    plt.imshow(i.edgeDetection(55, 6))
    plt.show()