"""
binary search
"""
import random
import time
import math

def binary_search(lst:list[int|float], itm:int|float)->tuple[int, int]:
    """return index of itm in lst"""
    
    cut_by = len(lst) // 2
    curnt_indx = 0 

    i = 0

    while True:
        curnt_indx += cut_by

        crnt_comp = lst[curnt_indx]
     
        if crnt_comp == itm:
            return curnt_indx, i

        if crnt_comp > itm:
            cut_by = min(-(cut_by // 2), -1) 
        else:
            cut_by = max(abs(cut_by) // 2, 1)

        i += 1
        #print(f"current cut: {cut_by, curnt_indx}")
        #print(f"current cpm: {crnt_comp}")
        
        #time.sleep(1)

MAX_VAL = 1000000
LEN = 100
REPS = 1000

i_lst = []
for _ in range(REPS):
    sorted_list = sorted([random.randint(0, MAX_VAL) for _ in range(LEN)])
    search_element = sorted_list[random.randint(0, LEN-1)]

    #print(sorted_list)
    #print(search_element)

    rs = binary_search(sorted_list, search_element)

    if sorted_list[rs[0]] == search_element:
        if rs[1] > math.ceil(math.log2(LEN)):

            print(f"test succes, with {rs[1]=}")
        i_lst.append(rs[1])
    else:
        print("error:")


print(sum(i_lst) / len(i_lst))

