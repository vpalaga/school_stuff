from PIL import Image, ImageDraw

import math

class Graph:
    def __init__(self, size=(500, 500)):
        # Create a blank white image
        self.size = size
        self.mid_pos = (size[0]/2, size[1]/2)

        self.img = Image.new("RGB", size, "white")

        # Create a drawing object
        self.draw = ImageDraw.Draw(self.img)

        self.colors = {
        1: (0, 0, 255),      # blue
        2: (0, 128, 0),      # green
        3: (255, 0, 0),      # red
        4: (0, 0, 128),      # dark blue
        5: (128, 0, 0),      # dark red
        6: (0, 128, 128),    # teal
        7: (0, 0, 0),        # black
        8: (128, 128, 128)   # gray
        } 

# Draw some lines
    def graph(self, max_val: float, start_at:float, values:list[float], length=0.7, lines=36000)->None:
        """
        draw.line((50, 50, 350, 50), fill="black", width=3)     # horizontal line
        draw.line((50, 100, 350, 300), fill="blue", width=5)    # diagonal line
        draw.line((50, 350, 350, 50), fill="red", width=2)      # another diagonal
        aa
        """
        line_len = length * self.mid_pos[0]
        current_sector = 0
        angle_multiplier = 360 / lines
        angle_prop = (max_val-start_at)/360
        current_color = self.colors[current_sector+1]

        values.insert(0,0)
        for alpha in range(lines):
            alpha *= angle_multiplier
            
            if current_sector < len(values)-1:
                if alpha*angle_prop >= values[current_sector+1] - start_at:
                    current_sector+=1
                    print(alpha)
                    current_color = self.colors[current_sector+1]
            
            alpha_rad = math.radians(alpha)

            line_end = (line_len * math.cos(alpha_rad - math.pi/2) + self.mid_pos[0], 
                        line_len * math.sin(alpha_rad - math.pi/2) + self.mid_pos[1])

            #draw line
            self.draw.line((*self.mid_pos,*line_end), fill=current_color, width=2)

        self.draw.circle(self.mid_pos, 5, (0,0,0))
        self.draw.circle(self.mid_pos, line_len, None, (0,0,0), 2)

    def show(self, save=True):
        # Save the image
        if save: self.img.save("lines_example.png")
        # Optional: show the image
        self.img.show()


if __name__ == "__main__":
    gr = Graph()
    gr.graph(max_val=140,start_at=7, values=[17,81,98,113,133])
    gr.show()