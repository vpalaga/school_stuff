import csv

from Scene import Scene
from Faces import Vertex, HeadingTo
from games.render.Camera import Cam
from Video import Video

import math

scene1 = Scene()
"""scene1.add_vertex(Vertex((-2, 2, -2)))
scene1.add_vertex(Vertex((2, 2, -2)))
scene1.add_vertex(Vertex((2, 6, -2)))
scene1.add_vertex(Vertex((-2, 6, -2)))

scene1.add_vertex(Vertex((-2, 2, 2)))
scene1.add_vertex(Vertex((2, 2, 2)))
scene1.add_vertex(Vertex((2, 6, 2)))
scene1.add_vertex(Vertex((-2, 6, 2)))

scene1.connect_vertexes_with_edge(1,2,3,4,1,5,6,2,6,7,3,7,8,4,8,5)
"""
scene1.sphere(Vertex((0,200,0)),radius=150)

cam = Cam(Vertex((0, 0, 0)), HeadingTo((0, 0)))

cam.render_from_top(scene=scene1)

"""for _ in range(2):
    for i in range(0,360):
        x = math.cos(math.radians(i))
        z = math.sin(math.radians(i))

        cam.update_position(Vertex((x,0,z)),heading=HeadingTo((0,0)))
        cam.render_front(scene=scene1)
"""
cam.render_front(scene1)

"""vid = Video(60)
vid.render(cam.frames)
"""