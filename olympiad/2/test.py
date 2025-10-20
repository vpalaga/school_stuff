
revers_d = {1: 0, 2: 3, 3: 0}

def reshape_roads_village_rarity(d):

    item_list = []
    for x, y in d.items():
        item_list += [x, y]

    occ = {}
    for i in range(max(item_list) + 1):
        occ[i] = item_list.count(i)

    print(occ)
    occ = dict(sorted(occ.items(), key=lambda x: x[1], reverse=True))
    print(occ)

    data_w_occ = {}

    for k, v in d.items():
        data_w_occ[(k, v)] = occ[k] + occ[v]

    data_w_occ = dict(sorted(data_w_occ.items(), key=lambda x: x[1], reverse=True))

    out = {}

    for d, _ in data_w_occ.items():
        out[d[0]] = d[1]

    return out

print(dct_oc(revers_d))