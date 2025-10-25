from collections import Counter

INPUT = {}
OUTPUT = ""

class Game:
    def __init__(self,
                 game_nr_ : int,
                 villages_: int,
                 roads_
                 ): # use _ under var name so pycharm doesn't fuck me :D

        self.nr = game_nr_
        self.villages = villages_
        self.roads = roads_
        """-----"""
        self.watchtowers = self.watchtowers()
        self.villages_reach_time = {}
        """-----"""
        self.solve_time = None
        self.solve()

    def watchtowers(self):
        villages = []
        for v_from, v_to in self.roads.items():
            villages.append(v_from)
            villages.append(v_to)

        counts = Counter(villages)

        # Sort by frequency (descending), then by value (optional)
        start_v = [item for item, count in counts.items() if count == 1 and item != 0]

        return start_v

    def solve(self):
        for watchtower in self.watchtowers:
            c_time = 0
            c_v = watchtower
            while c_v in self.roads.keys():
                c_time += 1
                c_v = self.roads[c_v]

                if c_v in self.villages_reach_time.keys():
                    if self.villages_reach_time[c_v] > c_time:
                        self.villages_reach_time[c_v] = c_time
                    else: # better time already exists
                        break
                else:
                    self.villages_reach_time[c_v] = c_time

        self.solve_time = sum(self.villages_reach_time.values())

with open("timuridriders-sub3-attempt2.txt", "r") as f:

    INPUT_RAW = [i.strip("\n") for i in f.readlines()]
    TEST_CASES = int(INPUT_RAW.pop(0))

raw_input_index = 0
for test_case in range(TEST_CASES): # crate a game object for each test segment of the input

    villages = int(INPUT_RAW[raw_input_index])

    raw_input_index += 1
    roads = {}
    weights = {}

    for road_nr in range(villages - 1):
        road_weight = INPUT_RAW[raw_input_index].split(" ")

        roads[road_nr + 1] = road_weight[0]
        weights

        raw_input_index += 1

    print(test_case)

    new_game = Game(test_case,
                    villages,
                    roads)

    INPUT[test_case] = new_game


for i, game in INPUT.items():

    OUTPUT += f"Case #{i}: {game.solve_time}\n"

print(OUTPUT)

open("output.txt", "w").write(OUTPUT)
