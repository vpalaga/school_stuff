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
        self.roads, self.road_lookup = self.extract_road_data()
        self.riders = riders_
        self.riders_release = riders_release_

        self.game_state = {x: None for x in range(self.villages)}
        self.riders_final_village = []

    def extract_road_data(self):
        roads_ret = []
        road_lookup = {}
        for i, road in enumerate(self.raw_roads):
            road_from = i + 1
            road_to = road[0]
            road_time = road[1]

            roads_ret.append(({road_from: road_to}, road_time))
            road_lookup[road_from] = road_to

        return roads_ret, road_lookup

    def show_stats(self):
        print(f"{self.nr}")
        print(f"    {self.villages=}")
        print(f"    {self.roads=}")
        print(f"    {self.riders=}")
        print(f"    {self.riders_release=}")
        print(f"    {self.road_lookup=}")

    def show_game_state(self):
        print(self.game_state)


    def dispatch_riders(self):

        for rider_nr, starting_pos in enumerate(self.riders_release):

            current_pos = starting_pos

            while self.game_state[self.road_lookup[current_pos]] is None: # check is the next village on the tree is occupied
                current_pos = self.road_lookup[current_pos]
                if current_pos == 0: #  or reached capital
                    break

            self.game_state[current_pos] = rider_nr
            self.riders_final_village.append(current_pos)




with open("input.txt", "r") as f:

    INPUT_RAW = [i.strip("\n") for i in f.readlines()]
    TEST_CASES = int(INPUT_RAW.pop(0))


for test_case in range(TEST_CASES): # crate a game object for each test segment of the input

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
    game.show_stats()
    #game.show_game_state()

    game.dispatch_riders()
    print(game.riders_final_village)
    OUTPUT += f"Case #{i}: {' '.join([str(x) for x in game.riders_final_village])}\n"

print(OUTPUT)

open("output.txt", "w").write(OUTPUT)