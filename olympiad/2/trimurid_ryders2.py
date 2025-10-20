import numpy as np

INPUT = {}
OUTPUT = ""

class Game:
    def __init__(self,
                 game_nr_ : int,
                 villages_: int,
                 roads_: list[tuple[int,int]],
                 riders_: int,
                 riders_release_: list[int]): # use _ under var name so pycharm doesn't fuck me :D

        self.nr = game_nr_
        self.villages = villages_
        self.raw_roads = roads_
        self.roads, self.road_lookup, self.road_to_time_lookup = self.extract_road_data()

        self.reverse_road_lookup = dict((v,k) for k,v in self.road_lookup.items())
        #self.time_lookup = self.build_road()
        self.riders = riders_
        self.riders_release = riders_release_

        self.game_state = {x: None for x in range(self.villages)}
        self.riders_final_village = []
        self.total_ride_time = 0

    def extract_road_data(self):
        roads_ret = []
        road_lookup = {}
        road_to_time_lookup = {}
        for i, road in enumerate(self.raw_roads):
            road_from = i + 1
            road_to = road[0]
            road_time = road[1]

            roads_ret.append(({road_from: road_to}, road_time))
            road_lookup[road_from] = road_to
            road_to_time_lookup[road_from] = road_time

        return roads_ret, road_lookup, road_to_time_lookup #np.array(list(reversed(time_lookup)))

    def show_stats(self):
        print(f"{self.nr}")
        print(f"    {self.villages=}")
        print(f"    {self.roads=}")
        print(f"    {self.riders=}")
        print(f"    {self.riders_release=}")
        print(f"    {self.road_lookup=}")


    def build_road(self):
        time_lookup = []
        current_village = 0
        for _ in range(self.villages - 1):
            current_village = self.reverse_road_lookup[current_village]
            time_lookup.append(self.road_to_time_lookup[current_village])

        return np.array(list(reversed(time_lookup)))

    def sum_ride_times(self):

        #print(self.time_lookup)
        prefix_sum = [0]
        for t in self.time_lookup:
            prefix_sum.append(prefix_sum[-1] + t)
        # sum all prefix sums except the first 0
        self.total_ride_time = sum(prefix_sum[1:])

with open("test.txt", "r") as f:

    INPUT_RAW = [i.strip("\n") for i in f.readlines()]
    TEST_CASES = int(INPUT_RAW.pop(0))

raw_input_index = 0
#print(TEST_CASES)
for test_case in range(TEST_CASES): # crate a game object for each test segment of the input

    villages = int(INPUT_RAW[raw_input_index])

    raw_input_index += 1
    roads = []
    for road_nr in range(villages - 1):
        roads.append(list(int(x) for x in INPUT_RAW[raw_input_index].split(" ")))

        raw_input_index += 1

    print(test_case)

    new_game = Game(test_case,
                    villages,
                    roads,
                    villages - 1,
                    [villages - 1]*(villages - 1))

    INPUT[test_case] = new_game

for i, game in INPUT.items():

    game.show_stats()
    game.sum_ride_times()
    #game.show_stats()
    print(i, game.total_ride_time)
    #print(game.time_lookup)
    OUTPUT += f"Case #{i}: {game.total_ride_time}\n"

print(OUTPUT)

open("output.txt", "w").write(OUTPUT)