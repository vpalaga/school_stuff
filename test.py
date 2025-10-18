import math

print(math.sin(30 * (math.pi/180)))
for n in range(10):
    a = math.sin(n*10  * (math.pi/180))*5.2
    print(f"{n}: {round(a, ndigits=1)}")

from partitions import Pa