from Faces import Vertex, Edge, Face
from typing import Dict
import math

class Scene:
    def __init__(self):
        self.models = self.Models(self)

        self.objects: Dict[int,Vertex|Edge|Face] = {}
        self.objects_index_sorted_by_distance: Dict[int,float] = {}

    def add_object(self,element:Vertex|Edge|Face)->None:
        self.objects[len(self.objects)+1] = element

    def connect_vertexes_with_edge(self,*vertexes_index:int)->None:
        vertexes = {}
        for i, item in self.objects.items():
            if type(item) is Vertex:
                vertexes[i] = item

        for i in range(len(vertexes_index)-1):
            try:
                self.add_object(Edge(vertexes[vertexes_index[i]], vertexes[vertexes_index[i+1]]))
            except KeyError:
                print(f"unable to add Edge between V:{vertexes_index[i]} and V:{vertexes_index[i+1]}")

    def sort_vertexes_by_distance_from_vertex(self,origin:Vertex)->dict[int,float]:
        index_distance = {}
        for index, item in self.objects.items():
            dx = item.mid_point[0] - origin.x
            dy = item.mid_point[1] - origin.y
            dz = item.mid_point[2] - origin.z

            index_distance[index] = math.hypot(dx,dy,dz)

        # sort descending, so the last gets rendered last
        return dict(
            sorted(index_distance.items(), key=lambda i: i[1], reverse=True)
        )

    def sort_objects_by_distance(self,origin:Vertex)->None:
        self.objects_index_sorted_by_distance = self.sort_vertexes_by_distance_from_vertex(origin)

    class Models:
        def __init__(self,scene:Scene)->None:
            self.scene = scene

        def sphere(self, origin: Vertex, radius: float) -> None:
            for theta in range(0, 360):  # around (longitude)
                for phi in range(0, 181):  # top to bottom (latitude)

                    theta_rad = math.radians(theta)
                    phi_rad = math.radians(phi)

                    x = origin.x + radius * math.sin(phi_rad) * math.cos(theta_rad)
                    y = origin.y + radius * math.sin(phi_rad) * math.sin(theta_rad)
                    z = origin.z + radius * math.cos(phi_rad)

                    self.scene.add_object(Vertex((x, y, z)))

        def block(self,origin:Vertex,size:Vertex,mode:str)->None:
            pass