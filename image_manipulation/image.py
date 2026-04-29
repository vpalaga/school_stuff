import cv2
import math
from typing import Tuple
import time


def calc_avg_color(src, origin: tuple[int, int], sides: tuple[int, int]) -> tuple[int, int, int]:
    x0, y0 = origin
    w, h = sides

    H, W = src.shape[:2]

    # Clamp region to image bounds
    x1 = max(0, x0)
    y1 = max(0, y0)
    x2 = min(W, x0 + w)
    y2 = min(H, y0 + h)

    roi = src[y1:y2, x1:x2]

    if roi.size == 0:
        return 0, 0, 0

    # OpenCV uses BGR
    r, g, b = roi.mean(axis=(0, 1))
    return round(float(r)), round(float(g)), round(float(b))


def avg_black_scale(src, origin: tuple[int, int], sides: tuple[int, int]) -> tuple[int, int, int]:
    avg_color = calc_avg_color(src=src,
                                    origin=origin,
                                    sides=sides)
    bgr_color = (avg_color[2], avg_color[1], avg_color[0])

    b = max(min(sum(bgr_color) // 3, 255), 0)
    return b, b, b


class Feed:
    def __init__(self):

        self.blocks_width = 100
        self.shift = -120

        # Open the default camera
        self.cam = cv2.VideoCapture(0)


        # Get the default frame width and height
        self.frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(self.frame_width, self.frame_height)

        self.x_field = self.frame_width / self.blocks_width
        self.y_field = self.x_field * 2

        # floor y down to a real number
        self.size = (self.blocks_width, math.floor(self.frame_height / self.y_field))
        print(self.size)

    def calc_size(self):
        self.x_field = self.frame_width / self.blocks_width
        self.y_field = self.x_field * 2

        # floor y down to a real number
        self.size = (self.blocks_width, math.floor(self.frame_height / self.y_field))


    def work(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        new_frame = frame.copy()
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                xr = int(self.x_field * x)
                yr = int(self.y_field * y)

                black_white = self.avg_black_scale(image_rgb, (xr,yr), (int(self.x_field),int(self.y_field)))

                cv2.rectangle(
                    new_frame,
                    (xr, yr),
                    (int(xr + self.x_field), int(yr + self.y_field)),
                    black_white,
                    -1  # fill rectangle (important!)
                )
        return new_frame
    def start(self):
        while True:
            ret, frame = self.cam.read()

            nframe = self.work(frame)

            # Display the captured frame
            cv2.imshow('Camera', nframe)

            # Press 'q' to exit the loop
            if cv2.waitKey(1) == ord('q'):
                break

        # Release the capture and writer objects
        self.cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    f = Feed()
    f.start()