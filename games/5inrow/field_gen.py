class Playground:
    def __init__(self, size: tuple[int,int], pixels:tuple[int,int]):
        self.size = size
        self.pixels = pixels

        self.xField = pixels[0] / size[0]
        self.yField = pixels[1] / size[1]

        self.mid_pos = {}
        self.state = {}

        self.gen_midpos()
        self.populate_state()

    def populate_state(self):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.state[(x, y)] = None

    def gen_midpos(self):
        nx = self.xField / 2
        ny = self.yField / 2

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                self.mid_pos[(x, y)] = (nx,ny)
                nx += self.xField
            nx = self.xField / 2
            ny += self.yField

    def count_in_row(self,pos:tuple[int,int], heading:tuple[int,int])->int:
        x, y = pos
        at_pos = self.state[pos]
        # unoccuped space
        if at_pos is None:
            return 0
        c = 1

        for _ in range(4):
            x += heading[0]
            y += heading[1]

            # have changed -> cant be in row
            try:
                if at_pos != self.state[(x, y)]:
                    return c

                at_pos = self.state[pos]
                c+=1

            except KeyError:
                break

        return c

    def check_for_wins(self)->None|tuple[tuple[int,int],tuple[int,int]]:
        check_directions = [(1, 0), (0,1), (1, 1), (-1, 1)]
        for y in range(self.size[1]):
            for x in range(self.size[0]):

                for heading in check_directions:

                    in_row_count = self.count_in_row((x, y), heading)

                    if in_row_count == 5:
                        return (x, y), (x + heading[0] * 4, y + heading[1] * 4)

        return None
