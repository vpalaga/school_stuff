from path_alg import Path
"""path_alg.py:
#note: replace "" with the actual triple quoted string

def sort_dict(d, by_key=True):
    if by_key:
        return dict(sorted(d.items(), key=lambda item: item[1]))
    return dict(sorted(d.items()))

def fire_time(f1:tuple[int, int], f2:tuple[int, int]) -> int:
    ""
    find the time for fire1(f1) to connect with fire2(f2):

    Answer key: time for Fire to get point A = minimal path distance from F to A

    1)  find the x y components of the difference : |x1-x2|, |y1-y2|
    2)  subtract 1 from each component to get rid of the corner,
        and the abs() does deal with cases where y or x component is 0: 0-1 = -1 -> 1
    3)  we can assign each number from x y components to the f1->f2 path,
        but as we will notice there is allways one path piece missing in the x or y component
        so we add it back as well we add the components together to add the total path distance,
    4)  We have to divide the distance by 2 since the fire is spreading from both sides.
    5)  In case distance is odd: (distance mod 2 == 1), we have to get rid of the 1 path piece we added since we cannot
        pass through path tiles diagonally, I do this by rounding DOWN to nearest integer.
        (be careful when using round() with n + 0.5, the output is a result "banker’s rounding")
    ""
    x1, y1 = f1
    x2, y2 = f2

    x_c, y_c = abs(x1 - x2), abs(y1 - y2)
    x_c, y_c = x_c - 1, y_c - 1

    if x_c < 0:
        x_c = 0
    if y_c < 0:
        y_c = 0

    return round((x_c + y_c + 1) / 2 - 0.1)

def dist_from_S_E(x, y, n, ret_node_from=False):
    ""
    Returns the x, y pos to minimal start node and end node
    start, end""

    if not ret_node_from: # dont calc the node pos if not needed
        return min(x, n - y -1 ), min(y, n - x - 1)

    if x < n - y - 1:
        ret_x = (-1, y)
    else:
        ret_x = (x, n)

    if y < n - x - 1:
        ret_y = (x, -1)
    else:
        ret_y = (n, y)

    return ret_x, ret_y, min(x, n - y - 1 ), min(y, n - x - 1)

def build_fire_tree(fire_dict, n, m):
    tree = {}
    paths = {}
    end_paths = {}
    weights = []

    for i, fire in fire_dict.items():
        s, e = dist_from_S_E(*fire, n=n)
        paths[i] = s
        end_paths[i] = e

        for x in (s, e):
            if x not in weights:
                weights.append(x) # add start and end weights but only when original

    tree[-1] = paths  # add the paths to each node

    for i, fire in fire_dict.items():
        paths = {}

        for ii in range(m):
            if i != ii:
                fire_t = fire_time(fire, fire_dict[ii])
                paths[ii] = fire_t

                if fire_t not in weights:
                    weights.append(fire_t)

        paths[m] = end_paths[i]
        tree[i] = paths

    tree[m] = {}
    return tree, sorted(weights)

class Path:
    def __init__(self, fire_dict_, n_:int):
        self.fire_dict = fire_dict_
        self.n = n_

        self.m = len(self.fire_dict)
        self.fire_tree, self.weights = build_fire_tree(self.fire_dict, n=self.n,  m=self.m)
        ""-------------------------""
        self.max_path_weight = min(self.fire_tree[-1].values())  # get the smallest starting weight
        self.weights = self.weights[self.weights.index(self.max_path_weight):] # cut off the start of weights
        ""-------------------------""
        self.find_path()

    def find_path(self):
        ""
        Parameters:
        ----------

        fires: a list with all the fire nodes positions [(x,y) ...]

        Returns
        -------
        path: [nodes to take from -1 to m, so min(path) is as small as possible]
        max_w = the maximal path length in the path

        Description:
        -------
        1)

        ""
        accessible_nodes = [-1]

        for weight in self.weights:

            list_changed = True
            while list_changed:
                accessible_nodes, list_changed = self.accessible_nodes_f(accessible_nodes)

                if self.m in accessible_nodes:
                    return

            self.max_path_weight = weight

        return

    def accessible_nodes_f(self, start_nodes:list[int]):
        ""returns: an expanded list of the start nodes""
        accessible_nodes = start_nodes.copy()
        list_changed = False

        for node in start_nodes:
            for node_test, weight in self.fire_tree[node].items():
                if weight <= self.max_path_weight:
                    if node_test not in accessible_nodes: # dont append if redundant
                        accessible_nodes.append(node_test)
                        list_changed = True

        return accessible_nodes, list_changed

"""


GAME_DATA = {}
OUTPUT = ""

class Game:
    def __init__(self, n_,m_, fires_):
        self.n = n_
        self.m = m_
        self.fires = fires_

        self.fire_dict = {i: xy for i, xy in enumerate(self.fires)}

        self.max_time = Path(self.fire_dict, self.n).max_path_weight - 1


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

    OUTPUT += f"Case #{i}: {game.max_time}\n"

print(OUTPUT)

open("output.txt", "w").write(OUTPUT)