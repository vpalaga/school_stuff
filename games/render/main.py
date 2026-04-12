from Scene import Scene
from Faces import Vertex, HeadingTo
from Camera import Cam

scene1 = Scene()
scene1.add_vertex(Vertex((1, 4, 0), 0))

cam = Cam(Vertex((0, 0, 0)), HeadingTo((0, 0)))
cam.render_from_top(scene=scene1)
