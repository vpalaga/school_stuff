import numpy as np

INPUT = {}
OUTPUT = ""

"""class Village:
    def __init__(self, leaving_ : int, incoming_: list[int], nr_, path_to_tower: int):
        self.incoming = incoming_
        self.leaving = leaving_
        self.nr = nr_

        self.path_to_tower_cof = path_to_tower

"""
class Game:
    def __init__(self,
                 game_nr_ : int,
                 villages_: int,
                 roads_: list[tuple[int,int]]
                 ): # use _ under var name so pycharm doesn't fuck me :D

        self.nr = game_nr_
        self.villages = villages_
        self.raw_roads = roads_

        self.roads, self.road_lookup = self.extract_road_data()

        self.total_ride_time = self.sum_ride_times()

    def extract_road_data(self):
        roads_ret = []
        road_lookup = {}
        for i, road in enumerate(self.raw_roads):
            road_from = i + 1
            road_to = road[0]
            road_time = road[1]

            roads_ret.append(({road_from: road_to}, road_time))
            road_lookup[road_from] = road_to


        return roads_ret, reshape_roads_village_rarity(road_lookup)

    def show_stats(self):
        print(f"{self.nr}")
        print(f"    {self.villages=}")
        print(f"    {self.roads=}")
        print(f"    {self.road_lookup=}")



    def sum_ride_times(self):

        revers_d = dict((v,k) for k,v in self.road_lookup.items())

        return chains(revers_d) # use pyramid theory to calc the fuck repeated roads


def chains(data):
    all_values = set(data.values())
    visited = set()
    lengths = []

    for k in data:
        # Only start from keys that aren't values
        if k in all_values or k in visited:
            continue

        length = 1
        visited.add(k)
        current = data[k]

        while current in data and current not in visited:
            visited.add(current)
            length += 1
            current = data[current]

        lengths.append(length)

    # Add isolated keys not visited
    for k in data:
        if k not in visited:
            lengths.append(1)

    total_time = 0
    for l in lengths:
        total_time += l*(l + 1) / 2

    return int(total_time)


def reshape_roads_village_rarity(d):
    data_w_occ = {}

    item_list = []
    for x, y in d.items():
        item_list += [x, y] # make a list with all keys and values

    occ = {}
    for i in range(max(item_list) + 1):
        occ[i] = item_list.count(i) # map the occurrence to a dict

    for k, v in d.items(): # make an occurrence map for the roads
        data_w_occ[(k, v)] = occ[k] + occ[v]

    data_w_occ = dict(sorted(data_w_occ.items(), key=lambda x: x[1], reverse=True)) # sort based on the occurrence

    out = {}

    for d, _ in data_w_occ.items(): # back to roads
        out[d[0]] = d[1]

    return out


with open("test.txt", "r") as f:

    INPUT_RAW = [i.strip("\n") for i in f.readlines()]
    TEST_CASES = int(INPUT_RAW.pop(0))

raw_input_index = 0
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
                    roads)

    INPUT[test_case] = new_game


for i, game in INPUT.items():

    game.show_stats()
    print(i, game.total_ride_time)
    #print(game.time_lookup)
    OUTPUT += f"Case #{i}: {game.total_ride_time}\n"

print(OUTPUT)

open("output.txt", "w").write(OUTPUT)