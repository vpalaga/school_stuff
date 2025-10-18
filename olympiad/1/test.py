

l1 = list(range(5))


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


print(split_list(l1, [2, 1, 2]))