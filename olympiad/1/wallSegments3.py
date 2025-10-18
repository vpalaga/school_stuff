INPUT = []
OUTPUT = ""
save_segment_splits = {}
example = 7
with open("input.txt", "r") as f:

    INPUT_RAW = [i.strip("\n") for i in f.readlines()]
    TEST_CASES = INPUT_RAW.pop(0)

    for _, i in enumerate(INPUT_RAW):
        if " " in i: # filter out the output states
            INPUT.append([int(n) for n in i.split(" ")]) # int from str


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


def arrange(input_list: list[int]):
    print(input_list)
    n = len(input_list)

    segment_lengths = []

    segment_length = 0
    for i in range(1, n):
        segment_length += 1
        if input_list[i] - input_list[i-1] != -1: # split the list into descending lists
            segment_lengths.append(segment_length)
            segment_length = 0

    segment_lengths.append(n - sum(segment_lengths)) # add the last segment end
    segments = split_list(input_list, segment_lengths)
    flipped = flip_list(segments)

    if list(range(n)) == flipped and sum(segment_lengths)==n:
        return segment_lengths
    return None

for n, test in enumerate(INPUT):
    segment_split = arrange(test)

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

open("output.txt", "w").write(OUTPUT)