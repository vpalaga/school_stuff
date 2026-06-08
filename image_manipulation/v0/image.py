import cv2
import math

from loader import Images, Img
from clalc import avg_black_scale

class Feed:
    def __init__(self):

        self.blocks_width = 30
        self.shift = -50

        self.desired_darkness = 50

        self.prin = True

        # Open the default camera
        self.cam = cv2.VideoCapture(0)

        self.images = Images(r"../source/ascii")

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

                black_white = avg_black_scale(image_rgb, (xr,yr), (int(self.x_field),int(self.y_field)))
                black_white = black_white[0] + self.shift, black_white[1] + self.shift, black_white[2] + self.shift
                img = self.images.find_best_image(black_white).image

                print(black_white[0])

                if False:
                    cv2.rectangle(
                        new_frame,
                        (xr, yr),
                        (int(xr + self.x_field), int(yr + self.y_field)),
                        black_white,
                        -1  # fill rectangle (important!)
                    )

                img = cv2.resize(img, (round(self.x_field), round(self.y_field)))

                h, w = img.shape[:2]
                try:
                    if (self.prin):
                        new_frame[yr:yr + h, xr:xr + w] = img
                except ValueError:
                    pass

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