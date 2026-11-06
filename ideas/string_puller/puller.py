import math

from Vis import Img
from Vector import Vec2

i = Img()

nodes = 5
r = 1
a = 2*math.pi / nodes

for n in range(nodes):
    alpha = a*n

    vec = Vec2(
        r * math.sin(alpha),
        r * math.cos(alpha)
    )

    i.add_object(vec)

i.create()