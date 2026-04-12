from Faces import Vertex, Edge
from typing import Dict
class Scene:
    def __init__(self):
        self.vertexes: Dict[int,Vertex] = {}
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
