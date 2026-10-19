
filePath = "in.txt"

with open(filePath, "r") as f:
    lines = [i.strip() for i in f.readlines()]
    jobs = int(lines.pop(0))

data = []
for n in range(jobs):
    data.append([lines[2*n], lines[2*n +1]])

print(data)

def pathHoles(road:list[int], holes_fix:int)->int:
    # longest wwindow containing at most holes_fix ones
    best = 0
    left = 0
    holes = 0

    for right, cell in enumerate(road):
        holes += cell
        while holes > holes_fix:  # too many holes: shrink from the left
            holes -= road[left]
            left += 1
        best = max(best, right - left + 1)

    return best

def process(task:list[str])->str:
    _, holesToFix = tuple(task[0].split(" "))
    holesToFix = int(holesToFix)
    road = [int(i) for i in task[1].split(" ")]

    return str(pathHoles(road, holesToFix))

o = ""
for n, t in enumerate(data):
    r = process(t)
    o += f"Case #{n}: {r}\n"
    print(r)

print(o)

with open("outp.txt", "w") as f:
    f.write(o)
