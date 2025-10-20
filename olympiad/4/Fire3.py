
GAME_DATA = {}
OUTPUT = ""

class Game:
    def __init__(self, n_,m_, fires_):
        self.n = n_
        self.m = m_
        self.fires = fires_

        self.fire_dict = {i: xy for i, xy in enumerate(self.fires)}

        self.fire_tree = self.build_fire_tree()
        self.path, self.t = self.calc_time()
        #print(self.fire_tree)


    def build_fire_tree(self):
        tree = {}
        paths = {}
        end_paths = {}

        for i, fire in self.fire_dict.items():
            s, e = self.dist_from_S_E(*fire)
            paths[i] = s
            end_paths[i] = e
        #print(end_paths)
        tree[-1] = paths # add the paths to each node

        for i, fire in self.fire_dict.items():
            paths = {}

            for ii in range(self.m):
                if i != ii:
                    paths[ii] = fire_time(fire, self.fire_dict[ii])

            paths[self.m] = end_paths[i]
            tree[i] = paths

        tree[self.m] = {}
        return tree

    def calc_time(self):
        return minimax_path_dfs_sorted( self.fire_tree, -1, self.m)


    def dist_from_S_E(self, x, y):
        """start, end"""
        return min(x, self.n - y -1 ), min(y, self.n - x - 1)


def fire_time(f1:tuple[int, int], f2:tuple[int, int]) -> int:
    x1, y1 = f1
    x2, y2 = f2

    distance = abs(x1 - x2) + abs(y1 - y2) - 1
    return round(distance / 2)

def minimax_path_dfs_sorted(graph, start, end):
    best_max = float('inf')
    best_path = []

    def dfs(node, path, current_max, visited):
        nonlocal best_max, best_path
        if node == end:
            if current_max < best_max or (current_max == best_max and len(path) < len(best_path)):
                best_max = current_max
                best_path = path[:]
            return
        # Sort neighbors safely by converting keys to strings
        for neighbor, weight in sorted(graph[node].items(), key=lambda x: str(x[0])):
            if neighbor not in visited:
                dfs(neighbor, path + [neighbor], max(current_max, weight), visited | {neighbor})

    dfs(start, [start], 0, {start})
    return best_path, best_max - 1 #  since we want to get there

with open("input.txt", "r") as f:

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

    #print(game.fire_tree)
    #print(game.fire_dict)
    #print(game.path)
    OUTPUT += f"Case #{i}: {game.t}\n"

print(OUTPUT)

open("output.txt", "w").write(OUTPUT)