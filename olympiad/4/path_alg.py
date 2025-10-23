def sort_dict(d, by_key=True):
    if by_key:
        return dict(sorted(d.items(), key=lambda item: item[1]))
    return dict(sorted(d.items()))

def fire_time(f1:tuple[int, int], f2:tuple[int, int]) -> int:
    """
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
    """
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
    """
    Returns the x, y pos to minimal start node and end node
    start, end"""

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

def compute_fire_pair(pair):
    i, j, f1, f2 = pair
    return i, j, fire_time(f1, f2)

def build_fire_tree(fire_dict, n, m):
    import itertools
    from multiprocessing import Pool

    tree = {}
    weights = set()
    start_paths = {}
    end_paths = {}

    for i, fire in fire_dict.items():
        s, e = dist_from_S_E(*fire, n=n)
        start_paths[i] = s
        end_paths[i] = e
        weights.update((s, e))

    tree[-1] = start_paths

    # Compute all unique pairs
    pairs = [(i, j, fire_dict[i], fire_dict[j]) for i, j in itertools.combinations(fire_dict.keys(), 2)]

    with Pool() as p:
        results = p.map(compute_fire_pair, pairs)

    fire_times = {}
    for i, j, t in results:
        fire_times[(i, j)] = fire_times[(j, i)] = t
        weights.add(t)

    for i in fire_dict.keys():
        paths = {ii: fire_times[(i, ii)] for ii in fire_dict.keys() if i != ii}
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
        """-------------------------"""
        self.max_path_weight = min(self.fire_tree[-1].values())  # get the smallest starting weight
        self.weights = self.weights[self.weights.index(self.max_path_weight):] # cut off the start of weights
        """-------------------------"""
        self.find_path()

    def find_path(self):
        """
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

        """
        accessible_nodes = [-1]

        for weight in self.weights:

            list_changed = True
            while list_changed:
                accessible_nodes, list_changed = self.accessible_nodes_f(accessible_nodes)

                if self.m in accessible_nodes:
                    return

            self.max_path_weight = weight

        return

    def accessible_nodes_f(self, start_nodes:set[int]):
        """returns: an expanded list of the start nodes"""
        accessible_nodes = set(start_nodes)
        list_changed = False

        for node in start_nodes:

            if node != -1:
                if self.fire_tree[node][self.m] <= self.max_path_weight:
                    accessible_nodes.add(self.m)
                    break

            for node_test, weight in self.fire_tree[node].items():
                if weight <= self.max_path_weight:
                    if node_test not in accessible_nodes: # dont append if redundant
                        accessible_nodes.add(node_test)
                        list_changed = True

        return accessible_nodes, list_changed