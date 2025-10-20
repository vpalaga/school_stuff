GAME_DATA = {}
OUTPUT = ""

class Game:
    def __init__(self, n_,m_, fires_):
        self.n = n_
        self.m = m_
        self.fires = fires_

        self.t = self.calc_time()

    def calc_time(self):
        time = None
        for x, y in fires:
            time = self.walls(x, y)

        return time

    def walls(self, x, y):
        return min(
            max(self.n - x - 1, n - y - 1),
            max(x, y),
            max(x, self.n - x - 1),
            max(y, self.n - y - 1)
        ) - 1 # -1 cos the last time to w path

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