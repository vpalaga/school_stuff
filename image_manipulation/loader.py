import cv2
from image import avg_black_scale
from pathlib import Path
from typing import List

class Img:
    def __init__(self, path:str)->None:
        self.path = path
        self.name = self.path.split("/")[-1]
        print(f"loading {self.name}")

        self.image = cv2.imread(self.path)
        self.h, self.w = self.image.shape[:2]
        print(f"loading {self.name} | {self.w}:{self.h}")
        self.crop_to(100, 200)

        self.black_scale = avg_black_scale(self.image, (0,0), (self.w,self.h))
        print(self.black_scale)

    def __repr__(self):
        return f"{self.name}"

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

        directory = Path(in_dir)

        for file in directory.iterdir():
            if file.is_file():
                try:
                     self.images.append(Img(in_dir + "/" +  file.name))

                except ValueError:
                    continue

if __name__ == "__main__":
    img = Images(r"source/ascii")

    for file in img.images:
        print(file)