from importlib import import_module

import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from scipy.ndimage import gaussian_filter1d

import functools
from typing import List, Callable, Any, Dict, Literal, cast

import os

from tqdm import tqdm

from ImageCreator import ImageCreator

class Manipulate:
    class Tools:
        BLACK = 0,0,0
        WHITE = 255,255,255
        RED = 255,0,0

        colors = {
            0: (255, 0, 0),  # red
            1: (0, 255, 0),  # green
            2: (0, 0, 255),  # blue
            3: (255, 255, 0),  # yellow
            4: (0, 255, 255),  # cyan
            5: (255, 0, 255),  # magenta
            6: (128, 128, 128),  # gray
            7: (255, 165, 0),  # orange
            8: (128, 0, 128),  # purple
        }

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

        @staticmethod
        def colorDifference(color1: tuple[int, int, int], color2: tuple[int, int, int]) -> int:
            difference = 0
            for ch in range(3):
                difference += abs(int(color1[ch]) - int(color2[ch]))
            return difference

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

        # 3 color channels with 255 colors each
        self.colorAnalyse: tuple[dict[int, int], dict[int, int], dict[int, int]] = ({n:0 for n in range(256)}, {n:0 for n in range(256)}, {n:0 for n in range(256)})
        self.colorPeaks: List[tuple[int, int, int]] = []
        self.y_smooth = [np.array([]), np.array([]), np.array([])]
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
    def set_image(self, set_to: np.ndarray)->Image.Image:
        self.image = set_to
        return Image.fromarray(self.image)

    def _analyseColor(self, colorChanel:Literal[0, 1, 2])->None:
        for y in self.heightRange:
            for x in self.widthRange:
                try:
                    self.colorAnalyse[colorChanel][self.image[y, x][colorChanel]] += 1
                except KeyError: print("E: unknown color")
    def analyseColors(self)->None:
        self._analyseColor(0) # red
        self._analyseColor(1) # green
        self._analyseColor(2) # blue

    def _findColorPeakOnChanel(self,Ch:Literal[0,1,2], n:int) -> list[int]:

        x = np.array(sorted(self.colorAnalyse[Ch].keys()))
        y = np.array([self.colorAnalyse[Ch][i] for i in x])

        # smooth
        y_smooth = gaussian_filter1d(y, sigma=8)
        self.y_smooth[Ch] = y_smooth

        # --- 1. cumulative integral (trapezoidal rule) ---
        # dx = 1 since x is 0..255
        cumulative = np.cumsum((y_smooth[:-1] + y_smooth[1:]) / 2)

        # prepend 0 so it aligns with x
        cumulative = np.insert(cumulative, 0, 0)

        total_area = cumulative[-1]

        # --- 2. choose number of segments ---
        target_areas = np.linspace(0, total_area, n)

        # --- 3. find x positions where cumulative area hits targets ---
        points = np.interp(target_areas, cumulative, x)

        # round to integers
        points = np.rint(points).astype(int)

        return points.tolist()
    def findColorPeaks(self, n:int)->None:
        redPeaks   = self._findColorPeakOnChanel(0, n)
        greenPeaks = self._findColorPeakOnChanel(1, n)
        bluePeaks  = self._findColorPeakOnChanel(2, n)

        # combine individual color chanel peaks into color points
        for i in range(n):
            rgb = (redPeaks[i], greenPeaks[i], bluePeaks[i])
            self.colorPeaks.append(rgb)

    def showColors(self, colors:list[int])->np.ndarray:
        new_image = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)
        for y in self.heightRange:
            for x in self.widthRange:
                color = self.image[y, x][0]
                if color in colors:
                    new_image[y, x] = self.tools.colors[self.colorPeaks.index(color)]
        return new_image
    def plotColorAnalyse(self, showRaw:bool=False):
        x = list(self.colorAnalyse[0].keys())

        if showRaw:
            rRaw = list(self.colorAnalyse[0].values())
            gRaw = list(self.colorAnalyse[1].values())
            bRaw = list(self.colorAnalyse[2].values())

            plt.plot(x, rRaw, color="red")
            plt.plot(x, gRaw, color="green")
            plt.plot(x, bRaw, color="blue")

        plt.plot(x, self.y_smooth[0],color="red", label="smoothed R")
        plt.plot(x, self.y_smooth[1],color="green", label="smoothed G")
        plt.plot(x, self.y_smooth[2],color="blue", label="smoothed B")

        # plot colorPeaks
        peaksSeparated: List[list[int]] = [[],[],[]]
        for peak in self.colorPeaks:
            peaksSeparated[0].append(peak[0])
            peaksSeparated[1].append(peak[1])
            peaksSeparated[2].append(peak[2])

        plt.scatter(peaksSeparated[0], [self.y_smooth[0][c] for c in peaksSeparated[0]],color='red', s=40)
        plt.scatter(peaksSeparated[1], [self.y_smooth[1][c] for c in peaksSeparated[1]],color='green', s=40)
        plt.scatter(peaksSeparated[2], [self.y_smooth[2][c] for c in peaksSeparated[2]],color='blue', s=40)

        plt.xlabel("color")
        plt.ylabel("appearances")
        plt.title("color analyse")
        plt.show()


    def _closestPeak(self, color:tuple[int,int,int])->int:
        """return index of the closest peak in sorted peaks"""
        lastDiff = None
        i = 0
        while i < len(self.colorPeaks):
            # redefined to rbg from ggg
            colorDiff = self.tools.colorDifference(color, self.colorPeaks[i])

            if lastDiff is not None:
                if colorDiff < lastDiff:
                    lastDiff = colorDiff
                else:
                    return i - 1
            else:
                lastDiff = colorDiff
            i += 1
        return i - 1
    def groupToPeaks(self)->np.ndarray:
        new_image = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)
        for y in self.heightRange:
            for x in self.widthRange:
                filedVal:tuple[int,int,int] = self.image[y, x]
                peakIndex = self._closestPeak(filedVal)
                new_image[y, x] = self.colorPeaks[peakIndex]

        return new_image
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
    def black_white(self)->np.ndarray:
        new_image = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)

        for y in self.heightRange:
            for x in self.widthRange:
                new_image[y, x] = self.tools.black_white(self.image[y, x])
        return new_image

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
    def edge_detection_v2(self)->ndarray:
        edges: List[tuple[int,int]] = []
        edge_mask = np.zeros((self.HEIGHT, self.WIDTH, 3), dtype=np.uint8)

        def isEdge(_x:int,_y:int)->bool:
            originField = self.image[_y, _x]
            is_edge = False
            # check 8 around x, y
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    # laned at 0,0
                    if dy == dy == 0:
                        continue

                    x = _x + dx
                    y = _y + dy

                    if not self.tools.is_real_pos(x, y):
                        continue



                    fieldColor = self.image[y, x]
                    if self.tools.colorDifference(fieldColor , originField) > 0:

                        # check if any edges around
                        # will overpower is_edge return path
                        if (x, y) in edges:
                            return False

                        # in is darker
                        if self.tools.black_white(fieldColor) < self.tools.black_white(originField):
                            is_edge = True

            return is_edge

        for ax in self.widthRange:
            for ay in self.heightRange:
                if isEdge(ax, ay):
                    edges.append((ax, ay))
                    edge_mask[ay, ax] = self.tools.RED

        return edge_mask

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
    @save_history
    def blur(self, radius:int=3)->np.ndarray:
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
                    if not self.tools.is_real_pos(x, y):
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
        bar = tqdm(total=self.HEIGHT * self.WIDTH)

        for y in self.heightRange:
            for x in self.widthRange:
                blurredImageArray[y, x] = avg_color(x, y)
            bar.update(self.WIDTH)


        return self._fixEdgesAfterBlur(blurredImageArray, radius)

if __name__ == "__main__":
    c = ImageCreator((100,100))
    c.fill(255)
    c.circle((50,50), 30, 150)
    c.circle((25, 25), 15, 200)
    c.circle((75,75), 40, 40)
    manip = Manipulate("bilder/6a1336e5a51ae_download.jpg")

    plt.imshow(manip.image)
    plt.show()

    #plt.imshow(manip.edge_detection_v1(threshold=.5))
    plt.show()

    #manip.set_image(manip.black_white())
    manip.set_image(manip.blur(radius=2))
    manip.analyseColors()
    manip.findColorPeaks(n=3)
    manip.set_image(manip.groupToPeaks())

    plt.imshow(manip.edge_detection_v2())
    plt.show()

    manip.plotColorAnalyse()

    plt.imshow(manip.image)
    plt.show()

    #plt.imshow(manip.showColors(manip.colorPeaks))
    plt.show()

    print(manip.colorPeaks)

