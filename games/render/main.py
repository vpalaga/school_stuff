from Scene import Scene
from Faces import Vertex, HeadingTo
from Camera import Cam

scene1 = Scene()
scene1.add_vertex(Vertex((4, 4, 0), ))
scene1.add_vertex(Vertex((0, 4, 0), ))
scene1.add_vertex(Vertex((-4, 4, 0), ))
scene1.add_vertex(Vertex((-4, 9, 0), ))

cam = Cam(Vertex((0, 0, 0)), HeadingTo((20, 0)))
cam.render_from_top(scene=scene1)
cam.render_front(scene=scene1)