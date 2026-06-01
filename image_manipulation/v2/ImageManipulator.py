import numpy as np
from numpy import ndarray
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy.ndimage import gaussian_filter1d

from typing import List, Literal

import os

from tqdm import tqdm

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
        @staticmethod
        def isSameRBG(p1:tuple[int,int,int], p2:tuple[int,int,int])->bool:
            for ch in range(3):
                # compare each chanel
                if p1[ch] != p2[ch]:
                    return False
            return True


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

        self.originalImage:ndarray = self.image

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

    def printImage(self):
        """prints the current image in the terminal"""
        for y in self.heightRange:
            line = ""
            for x in self.widthRange:
                field = self.image[y,x]
                if not self.tools.isSameRBG(field, self.tools.RED):
                    line += "[ ]"
                else:
                    line += "[█]"
            print(line)

    def update_image(self, set_to: np.ndarray)->None:
        """set self.image to ndarray"""
        self.image = set_to
    def layoverArray(self, layover: ndarray, ignoreColor:tuple[int,int,int]=(255,0,0))->ndarray:
        """overlays an image:ndarray over self.image"""
        newImg = self.image.copy()

        for y in self.heightRange:
            for x in self.widthRange:
                layField = layover[y, x]
                if self.tools.isSameRBG(layField, ignoreColor):
                    newImg[y, x] = layField
        return newImg

    # edge time -------------------------------------------------------------

    def _analyseColor(self, colorChanel:Literal[0, 1, 2])->None:
        """count color appearances in the image in the selected color chanel"""
        print("analysing color Ch:" + str(colorChanel))
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
        """integrate the area under the selected color chanel and divide into n sectors
        source: OpenAI: GPT"""

        x = np.array(sorted(self.colorAnalyse[Ch].keys()))
        y = np.array([self.colorAnalyse[Ch][i] for i in x])

        # smooth
        y_smooth = gaussian_filter1d(y, sigma=5)
        self.y_smooth[Ch] = y_smooth

        # --- 1. cumulative integral (trapezoidal rule) ---
        # dx = 1 since x is 0..255
        cumulative = np.cumsum((y_smooth[:-1] + y_smooth[1:]) / 2)

        # prepend 0 so it aligns with x
        cumulative = np.insert(cumulative, 0, 0)

        total_area = cumulative[-1]

        # --- 2. choose number of segments ---
        target_areas = np.linspace(0, total_area, n)

        # --- 3. find x positions where the cumulative area hits targets ---
        points = np.interp(target_areas, cumulative, x)

        # round to integers
        points = np.rint(points).astype(int)

        return points.tolist()
    def findColorPeaks(self, n:int)->None:
        redPeaks   = self._findColorPeakOnChanel(0, n + 2)
        greenPeaks = self._findColorPeakOnChanel(1, n + 2)
        bluePeaks  = self._findColorPeakOnChanel(2, n + 2)

        # combine individual color chanel peaks into color points
        # leave out the very first and the very last peaks
        for i in range(1,n+1):
            rgb = (redPeaks[i], greenPeaks[i], bluePeaks[i])
            self.colorPeaks.append(rgb)

    def plotColorAnalyse(self, showRaw:bool=False, showApx:bool=True, showPts:bool=True):
        x = list(self.colorAnalyse[0].keys())

        if showRaw:
            rRaw = list(self.colorAnalyse[0].values())
            gRaw = list(self.colorAnalyse[1].values())
            bRaw = list(self.colorAnalyse[2].values())

            plt.plot(x, rRaw, color="red")
            plt.plot(x, gRaw, color="green")
            plt.plot(x, bRaw, color="blue")

        if showApx:
            plt.plot(x, self.y_smooth[0],color="red", label="smoothed R")
            plt.plot(x, self.y_smooth[1],color="green", label="smoothed G")
            plt.plot(x, self.y_smooth[2],color="blue", label="smoothed B")

        if showPts:
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

        print("grouping...")
        bar = tqdm(total=self.HEIGHT * self.WIDTH)


        for y in self.heightRange:
            for x in self.widthRange:
                filedVal:tuple[int,int,int] = self.image[y, x]
                peakIndex = self._closestPeak(filedVal)
                new_image[y, x] = self.colorPeaks[peakIndex]
            bar.update(self.WIDTH)
        return new_image

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

        print("edging...")
        bar = tqdm(total=self.HEIGHT * self.WIDTH)

        for ax in self.widthRange:
            for ay in self.heightRange:
                if isEdge(ax, ay):
                    edges.append((ax, ay))
                    edge_mask[ay, ax] = self.tools.RED
            bar.update(self.WIDTH)

        return edge_mask

    def filterSmallEdges(self, src:ndarray, minPixels: int)->ndarray:
        exploredPixels: List[tuple[int, int]] = []
        def setPixelsBlack(pixels: list[tuple[int,int]])->None:
            for _x, _y in pixels:
                src[_y, _x] = self.tools.BLACK
        def isEdge(_x:int, _y:int)->bool:
            p = src[_y, _x]
            for ch in range(3):
                if p[ch] != self.tools.RED[ch]:
                    return False
            return True
        def exploreEdge(_x:int, _y:int)->None:
            if not isEdge(_x, _y):
                return

            edges: List[tuple[int,int]] = [(_x, _y)]
            newEdges: List[tuple[int, int]] = [(_x, _y)]

            while True:#
                newEdgesNextRound: List[tuple[int, int]] = []
                # search each known edge pixel for new edge pixels
                for xPixel, yPixel in newEdges:
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            if dy == dx == 0:
                                continue
                            x = dx + xPixel
                            y = dy + yPixel

                            if not self.tools.is_real_pos(x, y):
                                continue

                            # already found edge
                            if (x, y) in edges:
                                continue

                            if isEdge(x, y):
                                newEdgesNextRound.append((x, y))
                                edges.append((x, y))

                            # set pixel as explored
                            exploredPixels.append((x, y))

                # check if any new edges have been found
                if len(newEdgesNextRound) == 0:
                    break

                newEdges = newEdgesNextRound
            if len(edges) < minPixels:
                setPixelsBlack(edges)

        for y in self.heightRange:
            for x in self.widthRange:
                if (x, y) not in exploredPixels:
                    exploreEdge(x, y)
        return src

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
    #manip = Manipulate(image=np.load("bilder/bluredFrosch.npy"))
    manip = Manipulate("bilder/tiger.jpg")

    #manip.update_image(manip.blur(radius=2))

    plt.imshow(manip.image)
    plt.show()

    plt.show()
    #np.save("bilder/bluredFrosch.npy", manip.image)

    manip.analyseColors()
    manip.findColorPeaks(n=2)
    manip.update_image(manip.groupToPeaks())

    plt.imshow(manip.image)
    plt.show()

    edges = manip.filterSmallEdges(manip.edge_detection_v2(), minPixels=30)
    manip.update_image(manip.originalImage) # revert to org
    manip.update_image(manip.layoverArray(edges))

    plt.imshow(manip.image, interpolation='nearest')
    plt.title("filtered")

    plt.show()

    #manip.printImage()

    manip.plotColorAnalyse(showRaw=False, showApx=True, showPts=True)
    print(manip.colorPeaks)
