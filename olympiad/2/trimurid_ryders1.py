from mpmath.ctx_mp_python import return_mpc

INPUT = {}
OUTPUT = ""

class Game:
    def __init__(self, game_nr, villages, roads, riders, riders_release):

        self.nr = game_nr

        self.villages = villages
        self.raw_roads = roads
        self.roads = self.extract_road_data()
        self.riders = riders
        self.riders_release = riders_release

        self.game_state = {x: None for x in range(self.villages)}


    def extract_road_data(self):
        roads_ret = []
        for i, road in enumerate(self.raw_roads):
            road_from = i + 1
            road_to = road[0]
            road_time = road[1]

            roads_ret.append(({road_from: road_to}, road_time))

        return roads_ret

    def show_stats(self):
        print(f"{self.nr}")
        print(f"    {self.villages=}")
        print(f"    {self.roads=}")
        print(f"    {self.riders=}")
        print(f"    {self.riders_release=}")

    def show_game_state(self):
        print(self.game_state)


with open("input.txt", "r") as f:

    INPUT_RAW = [i.strip("\n") for i in f.readlines()]
    TEST_CASES = int(INPUT_RAW.pop(0))


for test_case in range(TEST_CASES):

    villages = int(INPUT_RAW.pop(0))

    roads = []
    for road_nr in range(villages - 1):
        roads.append(tuple(int(x) for x in INPUT_RAW.pop(0).split(" ")))
    riders = int(INPUT_RAW.pop(0))
    riders_release = [int(x) for x in INPUT_RAW.pop(0).split(" ")]

    new_game = Game(test_case,
                    villages,
                    roads,
                    riders,
                    riders_release)

    INPUT[test_case] = new_game

for i, game in INPUT.items():
    game.show_game_state()

print(OUTPUT)

open("output.txt", "w").write(OUTPUT)