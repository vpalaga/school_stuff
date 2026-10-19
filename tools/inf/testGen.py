import random
import time

l= []
srt = time.time()

for i in range(100):
    n = random.randint(0,1000)
    print(n)
    k = 0
    s =""
    for i in range(n):
        a = random.randint(0,1000)
        s += f"{a} "
        k += a
    print(s)

    l.append(k)

print("")
print("")
print("")


for r in l: print(r)
print("")
print("")
print("")

print(time.time() - srt)
