from Faces import Vertex, Edge
from typing import Dict
import math

class Scene:
    def __init__(self):
        self.vertexes: Dict[int,Vertex] = {}

        self.vertexes_index_sorted_by_distance: Dict[int,float] = {}

        self.edges: Dict[int,Edge] = {}

    def add_vertex(self,element:Vertex)->None:
        if element.vertex_number is not None:
            self.vertexes[element.vertex_number] = element
        else:
            self.vertexes[len(self.vertexes)+1] = element

    def add_edge(self,edge:Edge)->None:
        if edge.edge_number is not None:
            self.edges[edge.edge_number] = edge
        else:
            self.edges[len(self.edges)+1] = edge

    def connect_vertexes_with_edge(self,*vertexes_index:int)->None:
        for i in range(len(vertexes_index)-1):
            self.add_edge(Edge(self.vertexes[vertexes_index[i]], self.vertexes[vertexes_index[i+1]]))

    def sort_vertexes_by_distance_from_vertex(self,origin:Vertex)->None:
        index_distance = {}
        for index, vertex in self.vertexes.items():
            dx = vertex.x - origin.x
            dy = vertex.y - origin.y
            dz = vertex.z - origin.z
            index_distance[index] = math.hypot(dx,dy,dz)

        # sort descending, so the last gets rendered last
        self.vertexes_index_sorted_by_distance = dict(
            sorted(index_distance.items(), key=lambda item: item[1], reverse=True)
        )

        print(self.vertexes_index_sorted_by_distance)

    def sphere(self, origin: Vertex, radius: float) -> None:
        for theta in range(0, 360):  # around (longitude)
            for phi in range(0, 181):  # top to bottom (latitude)

                theta_rad = math.radians(theta)
                phi_rad = math.radians(phi)

                x = origin.x + radius * math.sin(phi_rad) * math.cos(theta_rad)
                y = origin.y + radius * math.sin(phi_rad) * math.sin(theta_rad)
                z = origin.z + radius * math.cos(phi_rad)

                self.add_vertex(Vertex((x, y, z)))
