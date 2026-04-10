class Vertex:
    def __init__(self, xyz: tuple[int,int,int],vert_num=None):
        self.xyz = xyz
        self.vertex_number = vert_num

        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]

        if len(xyz) > 3:
            raise ValueError(f"vls: {xyz}: too many values")

    def __repr__(self):
        return f"Vertex: x:{self.x} y:{self.y} z:{self.z}, {self.vertex_number=}"

if __name__ == "__main__":
    v1 = Vertex((1, 2, 3),0)
    print(v1)
