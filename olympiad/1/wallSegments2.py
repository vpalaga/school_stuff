INPUT = []
OUTPUT = ""

save_segment_splits = {}

with open("input.txt", "r") as f:

    INPUT_RAW = [i.strip("\n") for i in f.readlines()]
    TEST_CASES = INPUT_RAW.pop(0)

    for i in INPUT_RAW:
        if " " in i: # filter out the output states
            INPUT.append([int(n) for n in i.split(" ")]) # int from str


def segment_compositions(n: int, i=1): # use
    """
    use self-repeated function to calc all possible ways to split the list
    """
    if n == 0:
        return [[]]  # base case: empty list sums to 0
    result = []
    for k in range(1, n+1):
        for comp in segment_compositions(n - k):
            result.append([k] + comp)
    return result


def split_list(input_list: list[int], split_list_input_raw: list[int]):

    split_list_input = []
    total = 0
    for x in split_list_input_raw:
        total += x
        split_list_input.append(total) # find the cumulative sum of the split list

    output_lists = []

    for n in range(len(split_list_input)):
        if n == 0:  # define the segment start for first segment
            output_lists.append(input_list[0:split_list_input[n]])

        else:
            output_lists.append(input_list[split_list_input[n - 1]:split_list_input[n]])

    return output_lists


def flip_list(input_lists: list[list[int]]):
    """
    split the list at index and reverse individually=rotate
    """

    output_list = []

    for reverse_list in input_lists:
        output_list += reverse_list[::-1] # sum the reversed lists

    return output_list


def check_output(list_check: list[int]) -> list[int]|None:
    n = len(list_check)

    if n in save_segment_splits.keys():  # check is the length of the key was used, so we don't have to gen it.
        segment_splits = save_segment_splits[n]

    else: #gen it
        segment_splits = segment_compositions(n)
        save_segment_splits[n] = segment_splits # save it


    for segment_split in segment_splits:

        if flip_list(split_list(list(range(n)), segment_split)) == list_check:

            return segment_split

#    if list_check == [0, 1, 2]: # check default, because !!!can I choose to not flip??!!
#        return 1, [1] * len(list_check)

    return None


for n, test in enumerate(INPUT):
    segment_split = check_output(test)
    print(n)
    if segment_split is not None:

        string_segments = ""
        for segment in segment_split:
            string_segments += str(segment) + " "

        OUTPUT += f"Case #{n}: Possible\n"
        OUTPUT += f"{len(segment_split)}\n"
        OUTPUT += f"{string_segments}\n"

    else:
        OUTPUT += f"Case #{n}: Impossible\n"

    print(OUTPUT)
    OUTPUT = ""

open("output.txt", "w").write(OUTPUT)