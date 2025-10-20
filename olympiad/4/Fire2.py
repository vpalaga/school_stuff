from sympy import print_tree

GAME_DATA = {}
OUTPUT = ""

class Game:
    def __init__(self, n_,m_, fires_):
        self.n = n_
        self.m = m_
        self.fires = fires_
        self.sorted_fires = sorted([i[1] for i in self.fires])
        print(self.fires)

        self.t = self.calc_time()

    def calc_time(self):

        return min(
            self.max_fire_gap(),
            self.walls(self.fires[0][0] ,self.sorted_fires[0]), # check the first and last fire for the wall touching
            self.walls(self.fires[0][0] ,self.sorted_fires[-1])) - 1 # last possible escape

    def walls(self, x, y):
        return min(
            max(self.n - x - 1, n - y - 1),
            max(x, y),
            max(x, self.n - x - 1),
            max(y, self.n - y - 1)
        )

    def fire_time(self):
        gaps = []
        x_pos_list = sorted([-1] + [i[1] for i in self.fires] + [self.n]) # add n-1 element to calc the last gap as well

        for i in range(1, len(x_pos_list)):
            gap = x_pos_list[i] - x_pos_list[i-1] - 1
            if i == 1 or i == len(x_pos_list) - 1:
                pass
            else:
                gap *= 0.5 # unless on the edge, divide the gap by 2 since a fire comes from both sides
            gaps.append(round(gap + 0.01)) # work around so 0.5 rounded is 1 not 0

        return max(gaps) # return the biggest gap

    def vertical_time(self):
        return self.fires[0][0] # return the y value of first fire
with open("input.txt", "r") as f:

    INPUT_RAW = [i.strip("\n") for i in f.readlines()]
    TEST_CASES = int(INPUT_RAW.pop(0))

raw_input_index = 0
for test_case in range(TEST_CASES): # crate a game object for each test segment of the input
    fires = []

    n, m = tuple(int(x) for x in INPUT_RAW[raw_input_index].split(" "))

    for _ in range(m):
        raw_input_index += 1
        fires.append(tuple(int(x) for x in INPUT_RAW[raw_input_index].split(" ")))

    GAME_DATA[test_case] = Game(n, m, fires) # make an object for each test case

    raw_input_index += 1


for i, game in GAME_DATA.items():

    #print(game.fires)
    OUTPUT += f"Case #{i}: {game.t}\n"

print(OUTPUT)

open("output.txt", "w").write(OUTPUT)