import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

class Image:
    DEFAULT_IMAGE_PATH = r"bilder/frosch.jpg"
    def __init__(self, imagePath:None|str=None, imageData:None|ndarray=None):
        # load image from path if none are given
        if imageData is None:
            self.imagePath = imagePath if isinstance(imagePath, str) else self.DEFAULT_IMAGE_PATH
            self.image = self.load(self.imagePath)
        else:
            self.image = imageData
        # save original image for later edge mapping
        self.originalImage = self.image
        # for later usage
        self.HEIGHT, self.WIDTH = self.image.shape[:2]


    @staticmethod
    def load(path: str) -> ndarray:
        """load image as u_int8 ndarray[3] from the specified path"""

        # check if the image exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Image not found: {path}")

        # read
        img = mpimg.imread(path)
        # convert to correct type
        if img.dtype in (np.float32, np.float64):
            img = (img * 255).astype(np.uint8)
        else:
            img = img.astype(np.uint8)
        return img

    def colorDerivation(self,  threshold: int|float = 50.0)->ndarray:
        img_f = self.image
        grad_mag = np.zeros(img_f.shape[:2])

        # find the derivative each color channel
        for c in range(3):
            gy, gx = np.gradient(img_f[:, :, c])
            grad_mag += gx ** 2 + gy ** 2

        # Euclidean gradient magnitude
        grad_mag = np.sqrt(grad_mag)

        mask = grad_mag > threshold  # boolean array [y, x]
        ys, xs = np.where(mask)  # arrays of y and x coords
        coords = np.column_stack([ys, xs])  # shape [N, 2] — each row is [y, x]

        return coords

    def brightnessAdjust(self, setOff:float|int)->None:
        """offset each pixel of self.image by setOff"""
        setOff = np.array([setOff, setOff, setOff])  # R, G, B offsets
        self.image = np.clip(self.image+setOff,0,255)

    def _fixEdgesAfterBlur(self, image: np.ndarray, radius: int) -> np.ndarray:
        """fixes sides of the given image after a linear blur
        [protected method included in blur()] """
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

        # corners
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
        """blur self.image linearly:
        for each pixel imagine a square around it (s=2r+1),
        take the mean color of that square and set this color to the pixel
        returns: np.ndarray = img[y, x, c]
        """
        def is_real_pos(_x:int, _y:int)->bool:
            """checks whether given x, y coords are a valid image pixel position"""
            if 0<=_x<self.WIDTH and 0<=_y<self.HEIGHT:
                return True
            return False


        def avg_color(_x:int, _y:int)-> tuple[int, ...]:
            """return avg color of square round xy with side length of 2r+1
            returns: (int,int,int): avg color"""
            color = [0,0,0]
            fields = ((radius*2 + 1)**2)
            # for each pixel in this sub square
            for dy in range(-radius,radius+1):
                for dx in range(-radius,radius+1):
                    # skip center position
                    if dy == 0 and dx == 0:
                        continue
                    # calc absolute position in image
                    ax = _x + dx
                    ay = _y + dy
                    # check if the given pos is in the image
                    if not is_real_pos(ax, ay):
                        continue

                    # get pixel color
                    field = self.image[ay, ax]
                    # add each color channel to its sum
                    color[0] += int(field[0])
                    color[1] += int(field[1])
                    color[2] += int(field[2])

            avgColor: list[int] = [0,0,0]

            # calc avg of the collected pixel data in the square
            avgColor[0] = round(color[0] / fields)
            avgColor[1] = round(color[1] / fields)
            avgColor[2] = round(color[2] / fields)

            return tuple(avgColor)

        # new image, so we don't get interference when blur-ing
        blurredImageArray = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)

        # find blured color for each pixel and write it to the new image
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                blurredImageArray[y, x] = avg_color(x, y)

        # before returning, fix the edges and corners
        return self._fixEdgesAfterBlur(blurredImageArray, radius)

    def drawArray(self, b:ndarray)->None:
        """layover the given array onto self.image"""
        self.image[b[:, 0], b[:, 1]] = (255,0,0)

    def edgeDetection(self, t:int, r:int)->ndarray:
        """
        r: int -> blur radius
        t: int -> the lowest color change considered as edge.

        returns: ndarray image
        """
        # blur to reduce random noise
        self.blur(r)
        # find the derivative
        coords = self.colorDerivation(threshold=t)
        # lower image brightnes, so the plotted edges stand more out
        self.brightnessAdjust(-40)
        # plot the calculated coords
        self.drawArray(coords)
        # return the final image
        return self.image

if __name__ == "__main__":
    i = Image(r"bilder/500by500.jpg")
    plt.imshow(i.edgeDetection(55, 6))
    plt.show()