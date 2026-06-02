import math
import pickle
from os.path import isfile, join
from PIL import Image, ImageDraw
from generator import ImageLoader
from typing import Dict

class Build:
    FOLDER = "outputs"
    def __init__(self, name:str, blockSize:int=16):
        self.path = join(Build.FOLDER, name + ".png")
        self.blockSize = blockSize

        if not isfile(self.path): # file validation
            raise FileNotFoundError(f"{self.path} not valid")

        self.image = Image.open(self.path)
        self.imageRaw = ImageLoader.load(self.path)
        self.fitsBlocks:tuple[int,int] = self._calcBlocks()
        print(self.fitsBlocks)

        self.blockMap:dict[tuple[int,int], str] = pickle.load(open(self.path + ".pkl", "rb"))

    def _calcBlocks(self)->tuple[int,int]:
        h, w, ch = self.imageRaw.shape

        blockW:int = math.floor(w / self.blockSize)
        blockH:int = math.floor(h / self.blockSize)

        return blockW, blockH
    def show(self)->None:
        self.image.show()

    def splitIntoChunks(self, n:int=16)->None:
        h, w, ch = self.imageRaw.shape

        gapPixels = n * self.blockSize
        draw = ImageDraw.Draw(self.image)

        for x in range(self.fitsBlocks[0]):
            xPos = x * gapPixels
            draw.line((xPos, 0, xPos, h), fill="red", width=2)

        for y in range(self.fitsBlocks[1]):
            yPos = y * gapPixels
            draw.line((0, yPos, w, yPos), fill="red", width=2)
    def printMaterials(self)->None:
        materials: Dict[str, int] = {}

        for block in self.blockMap.values():
            try :
                materials[block] += 1
            except KeyError:
                materials[block] = 1

        materials = dict(sorted(materials.items(), key=lambda item: item[1], reverse=True))

        for block, amt in materials.items():
            print(f"{block:.<35}: {amt:<5}: {amt//64}s,{amt%64}i")

if __name__ == "__main__":
    b = Build("20")
    b.splitIntoChunks(n=16)
    b.printMaterials()
    b.show()