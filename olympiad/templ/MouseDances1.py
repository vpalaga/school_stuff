GAME_DATA = {}
OUTPUT = ""

class Game:
    def __init__(self):
        pass

with open("test.txt", "r") as f:

    INPUT_RAW = [i.strip("\n") for i in f.readlines()]
    TEST_CASES = int(INPUT_RAW.pop(0))


raw_input_index = 0

for test_case in range(TEST_CASES): # crate a game object for each test segment of the input
    print(test_case)


    GAME_DATA[test_case] = Game() # make an object for each test case

    raw_input_index += 1


for i, game in GAME_DATA.items():

    game.show_stats()

    OUTPUT += f"Case #{i}: {game.total_ride_time}\n"

print(OUTPUT)

open("output.txt", "w").write(OUTPUT)