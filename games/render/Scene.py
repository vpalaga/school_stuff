from Faces import Vertex
from typing import List

class Scene:
    def __init__(self, ):

            self.vertexes: List[Vertex] = []

    def add_vertex(self,element:Vertex):
        self.vertexes.append(element)
