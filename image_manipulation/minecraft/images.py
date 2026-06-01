import math

import numpy as np
from numpy import ndarray
from typing import List, Literal, Dict
from os import listdir
from os.path import isfile, join
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import time
from PIL import Image
from tqdm import tqdm


class Timer:
    def __init__(self)->None:
        self.startTime = time.time()
    def stop(self, n:int=2)->float|int:
        return round(time.time() - self.startTime, ndigits=n)

class Image:
    def __init__(self, name:str, number:int, imageData:ndarray, scaler:int=2)->None:
        self.name = name
        self.number = number
        self.imageData = self._scaleImage(imageData, scaler)

    @staticmethod
    def _scaleImage(srcDta:ndarray, scale:int)->ndarray:
        h, w, ch = srcDta.shape
        newImg = np.zeros((h * scale, w * scale, ch), dtype=np.uint8)

        for y in range(h):
            for x in range(w):
                newImg[y*scale:(y+1)*scale, x*scale:(x+1)*scale] = srcDta[y, x]

        return newImg

class Collection:
    def __init__(self, path:str, blockSize:int)->None:
        self.imageScaler = round(blockSize / 16) # round shouldn't be required

        self.images: List[Image] = self._loadImages(path, self.imageScaler)

    def __getitem__(self, item:int)->Image:
        return self.images[item]
    @staticmethod
    def _loadImages(path:str, scale:int)->list[Image]:

        timer = Timer()

        images: List[Image] = []
        for i, file in enumerate(listdir(path)):
            fullPath = join(path, file)
            if isfile(fullPath):
                image = (mpimg.imread(fullPath) * 255).astype(np.uint8)
                images.append(Image(name=file, number=i, imageData=image, scaler=scale))

        print(f"loaded {len(images)} images in {timer.stop()}s")
        return images

    @staticmethod
    def _imageDifference(image1:ndarray, image2:ndarray)->float|int:
        """return pixel diff. / pixels"""
        # check if both are same size
        if not image1.shape[0] == image2.shape[0] and image1.shape[1] == image2.shape[2]:
            print(image1.shape)
            print(image2.shape)
            raise ValueError("images are not the same")

        channels = int(min(image1.shape[2], image2.shape[2]))

        diffSum:int = 0
        for y in range(image1.shape[0]): # y-axis
            for x in range(image1.shape[1]): # x-axis
                for ch in range(channels): # color chanel
                    diffSum += abs(int(image1[y, x, ch]) - int(image2[y, x, ch]))
        return diffSum / int(image1.size)

    def bestBlock(self, matchImage:ndarray)->Image:
        bestImageMatch = self[0]
        bestImageMatchScore:None|float|int = None
        for compareImage in self.images:
            score = self._imageDifference(matchImage, compareImage.imageData)
            if bestImageMatchScore is not None:
                if bestImageMatchScore > score:
                    bestImageMatch = compareImage
            else:
                bestImageMatchScore = score

        return bestImageMatch

class Minecraft:
    def __init__(self, targetImagePath:str, blockSize:Literal[16,32,64])->None:
        self.targetImage = (mpimg.imread(targetImagePath) * 255).astype(np.uint8)
        self.blockSize = blockSize
        self.fitsBlocks:tuple[int,int] = self._findBlockDimensions()

        self.blockCollection = Collection(r"Blocks_1", blockSize)

        self.blockMap: Dict[tuple[int, int], str] = {}

    def _findBlockDimensions(self)->tuple[int,int]:
        h, w, ch = self.targetImage.shape

        blockW:int = math.floor(w / self.blockSize)
        blockH:int = math.floor(h / self.blockSize)

        return blockH, blockW

    def pixelate(self)->ndarray:
        newImg = np.zeros((self.fitsBlocks[0]*self.blockSize, self.fitsBlocks[1]*self.blockSize, 4), dtype=np.uint8)
        bar = tqdm(total=newImg.shape[0] * newImg.shape[1])


        for y in range(self.fitsBlocks[0]):
            for x in range(self.fitsBlocks[1]):
                # calc slices [y1: y2, x1: x2]
                y1 = y*self.blockSize
                y2 = (y+1)*self.blockSize
                x1 = x*self.blockSize
                x2 = (x+1)*self.blockSize

                currentImageSlice = self.targetImage[y1:y2, x1:x2]

                image = self.blockCollection.bestBlock(currentImageSlice)
                self.blockMap[(x, y)] = image.name

                newImg[y1:y2, x1:x2] = image.imageData
            bar.update(newImg.shape[0])

        Image.fromarray(newImg).save("Bilder/output.png")

        return newImg

if __name__ == "__main__":
    m = Minecraft("Bilder/Starry_Night.jpg", blockSize=16)
    plt.imshow(m.pixelate())
    plt.show()


