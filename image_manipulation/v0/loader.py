import turtle

import cv2
from clalc import avg_black_scale
from pathlib import Path
from typing import Dict, List

class Img:
    def __init__(self, path:str)->None:
        self.path = path
        self.name = self.path.split("/")[-1]

        self.char = chr(int(self.name.split(".")[0]))

        self.image = cv2.imread(self.path)
        self.h, self.w = self.image.shape[:2]

        self.black_scale = avg_black_scale(self.image, (0,0), (self.w,self.h))

    def __repr__(self):
        return f"{self.name}={self.char}, b:{self.black_scale}"

    def crop_to(self, width:int, height:int)->None:

        h = height // 2
        w = width // 2

        ih = self.h // 2
        iw = self.w // 2

        self.image = self.image[round(ih-h):round(ih+h),round(iw-w):round(iw+w)]

        #update
        self.h, self.w = self.image.shape[:2]

    def show(self):
        if self.image is not None:
            cv2.imshow(self.name, self.image)
            cv2.waitKey(0)

class Images:
    def __init__(self, in_dir:str)->None:

        self.images: List[Img] = []
        self.img_brightens = {}

        directory = Path(in_dir)

        for file in directory.iterdir():
            if file.is_file():
                try:
                     self.images.append(Img(in_dir + "/" +  file.name))

                except ValueError:
                    continue

        self.add_brightnesses()

    def add_brightnesses(self)->None:
        for img in self.images:
            self.img_brightens[img.name] = img.black_scale

        # sort by value

        self.img_brightens  = dict(
            sorted(self.img_brightens.items(), key=lambda i: i[1], reverse=False)
        )

    def find_best_image(self, b: tuple[int,int,int])->Img:
        best_image = self.images[0]

        for image in self.images[1:]:
            if abs(image.black_scale[0] - b[0]) < abs(best_image.black_scale[0] - b[0]):
                # better image found
                best_image = image

        return best_image

if __name__ == "__main__":
    img = Images(r"../source/ascii")
    print("looking for best match...")
    print(img.find_best_image(b=(200, 0,0)))