
GAME_DATA = {}
OUTPUT = ""

def ls_to_str(l):
    string_segments = ""
    for segment in l:
        string_segments += str(segment) + " "
    return string_segments

def find_optimal_line(circle):


    mice_ascending = []
    mice_descending = []

    for n in range(len(circle)): # try to find the normal distribution
        if n % 2 == 0:
            mice_descending.append(circle[n])
        else:
            mice_ascending.append(circle[n])

    return mice_ascending + sorted(mice_descending, reverse=True)

def inconvenience_from_sorted(l, find_m_line=False):
    max_inconvenience = 0
    inc = []

    for i in range(1, len(l)):
        inconvenience = abs(l[i-1] - l[i])
        inc.append(inconvenience)

        if inconvenience > max_inconvenience:
            max_inconvenience = inconvenience

    if not find_m_line:
        return max_inconvenience

    min_inconvenience = None
    split_at = None
    for split in range(len(l)): # brute it lol
        inc = max(inconvenience_from_sorted(find_optimal_line(l[0:int(split)])),
                  inconvenience_from_sorted(find_optimal_line(l[int(split):len(l)])))

        if min_inconvenience is not None:
            if inc < min_inconvenience:
                min_inconvenience = inc
                split_at = split
        else:
            min_inconvenience = inc

    return split_at

class Game:
    def __init__(self, nr_mice_, mice_heights_):
        self.n              = nr_mice_
        self.mice_heights   = mice_heights_

        self.heights_sorted = sorted(self.mice_heights)

        self.circle_a, self.circle_b = self.split_line()

        self.circle_a_o, self.circle_b_o = find_optimal_line(self.circle_a), find_optimal_line(self.circle_b)

        self.circle_a_i, self.circle_b_i = inconvenience_from_sorted(self.circle_a_o), inconvenience_from_sorted(self.circle_b_o)

        self.small_i = max(self.circle_a_i, self.circle_b_i)

        self.circle_len = [len(self.circle_a_o), len(self.circle_b_o)]

    def split_line(self):

        midline = inconvenience_from_sorted(self.heights_sorted, find_m_line=True)

        return self.heights_sorted[0:midline], self.heights_sorted[midline:self.n]


with open("test.txt", "r") as f:

    INPUT_RAW = [i.strip("\n") for i in f.readlines()]
    TEST_CASES = int(INPUT_RAW.pop(0))

raw_input_index = 0 # use raw index, so I don't have to shift the whole array
for test_case in range(TEST_CASES): # crate a game object for each test segment of the input

    n = int(INPUT_RAW[raw_input_index])
    raw_input_index += 1
    mice_heights = [int(x) for x in INPUT_RAW[raw_input_index].split(" ")]
    raw_input_index += 1

    GAME_DATA[test_case] = Game(n, mice_heights) # make an object for each test case

for i, game in GAME_DATA.items():
    pass

    OUTPUT += f"Case #{i}: {game.small_i}\n"
    OUTPUT += f"{ls_to_str(game.circle_len)}\n"
    OUTPUT += f"{ls_to_str(game.circle_a_o)}\n"
    OUTPUT += f"{ls_to_str(game.circle_b_o)}\n"

print(OUTPUT)

open("output.txt", "w").write(OUTPUT)