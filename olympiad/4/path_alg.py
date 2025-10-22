
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
    x_c, y_c = abs(x_c - 1), abs(y_c - 1)

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

    return ret_x, ret_y, min(x, n - y -1 ), min(y, n - x - 1)


def build_fire_tree(fire_dict, n, m):
    tree = {}
    paths = {}
    end_paths = {}

    for i, fire in fire_dict.items():
        s, e = dist_from_S_E(*fire, n=n)
        paths[i] = s
        end_paths[i] = e
    # print(end_paths)
    tree[-1] = paths  # add the paths to each node

    for i, fire in fire_dict.items():
        paths = {}

        for ii in range(m):
            if i != ii:
                paths[ii] = fire_time(fire, fire_dict[ii])

        paths[m] = end_paths[i]
        tree[i] = paths

    tree[m] = {}
    return tree

def find_path(fire_dict, n:int)-> list[int]:
    """

    Parameters:
    ----------

    fires: a list with all the fire nodes positions [(x,y) ...]

    Returns
    -------
    path: [nodes to take from -1 to m, so min(path) is as small as possible]

    Description:
    -------
    1)  Build a fire_tree with the data from each node to other nodes: {node.nr: {node.nr: length to node} ... }
    """
    m = len(fire_dict)
    fire_tree = build_fire_tree(fire_dict, n=n,  m=m)

    print(fire_tree)

    return [-1]