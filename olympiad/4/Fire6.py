from path_alg import Path
import os

GAME_DATA = {}
OUTPUT = ""

class Game:
    def __init__(self, n_,m_, fires_):
        self.n = n_
        self.m = m_
        self.fires = fires_

        self.fire_dict = {i: xy for i, xy in enumerate(self.fires)}

        self.max_time = Path(self.fire_dict, self.n).max_path_weight - 1


with open("test.txt", "r") as f:

    INPUT_RAW = [i.strip("\n") for i in f.readlines()]
    TEST_CASES = int(INPUT_RAW.pop(0))

raw_input_index = 0
for test_case in range(TEST_CASES): # crate a game object for each test segment of the input
    print(test_case)
    fires = []

    n, m = tuple(int(x) for x in INPUT_RAW[raw_input_index].split(" "))

    for _ in range(m):
        raw_input_index += 1
        fires.append(tuple(reversed(tuple(int(x) for x in INPUT_RAW[raw_input_index].split(" ")))))

    GAME_DATA[test_case] = Game(n, m, fires) # make an object for each test case

    raw_input_index += 1


for i, game in GAME_DATA.items():

    OUTPUT += f"Case #{i}: {game.max_time}\n"

print(OUTPUT)

open("output.txt", "w").write(OUTPUT)