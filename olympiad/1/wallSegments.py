INPUT = []
OUTPUT = ""
with open("input.txt", "r") as f:

    INPUT_RAW = [i.strip("\n") for i in f.readlines()]
    TEST_CASES = INPUT_RAW.pop(0)

    for i in INPUT_RAW:
        if " " in i: # filter out the output states
            INPUT.append([int(n) for n in i.split(" ")]) # int from str


def flip_list(flip_index: int):
    """
    split the list at index and reverse individually=rotate
    """
    a_list = [0, 1, 2][:flip_index]
    b_list = [0, 1, 2][flip_index:]

    return a_list[::-1] + b_list[::-1], [len(a_list), len(b_list)]

def check_output(list_check: list[int]):
    for i in range(len(list_check)):

        data_from_flip = flip_list(i)
        if data_from_flip[0] == list_check:

            return i, data_from_flip[1]

    if list_check == [0, 1, 2]: # check default, because !!!can I choose to not flip??!!
        return 1, [1, 1, 1]

    return False

"""
for n, test in enumerate(INPUT):
    i = check_output(test)

    if type(i) == tuple:

        segments = []
        for l in i[1]:
            if l > 0:
                segments.append(l)

        string_segments = ""
        for segment in segments:
            string_segments += str(segment) + " "


        OUTPUT += f"Case #{n}: Possible\n"
        OUTPUT += f"{len(segments)}\n"
        OUTPUT += f"{string_segments}\n"

    else:
        OUTPUT += f"Case #{n}: Impossible\n"

print(OUTPUT)

open("output.txt", "w").write(OUTPUT)
"""