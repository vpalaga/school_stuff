import string

d = {}
for i, l in enumerate(list(string.ascii_uppercase)):
    d[l] = i

def hash(s:str):
    n = 0
    for l in list(s):
        n += d[l]

    return list(d.keys())[n % 26], n%26

def okay_w(s:str)->bool:
    for l in list(w):
        if l not in list(d.keys()):
            return False
    return True

end = 10000
i = 0
h = hash("HALLO")
with open(r"6344203-a644cd4ddd6e423c0ebba49b76a58562b594e16b/6344203-a644cd4ddd6e423c0ebba49b76a58562b594e16b/common_german_word_list.txt", "r") as f:
    while True:
        w = f.readline().upper().strip()

        if okay_w(w):
            if hash(w) == h:
                print(w)

        i += 1
        if i> end:
            break