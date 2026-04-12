import math

class Vertex:
    def __init__(self, xyz: tuple[float,float,float], radius=.2, vert_num=None):
        self.xyz = xyz
        self.radius = radius
        self.vertex_number = vert_num

        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]

        if len(xyz) > 3:
            raise ValueError(f"vls: {xyz}: too many values")

    def global_angle_to_xy(self,origin:Vertex)->float:
        dx = self.x - origin.x
        dy = self.y - origin.y

        angle = math.degrees(math.atan(dx/dy))

        return angle

    def global_angle_to_yz(self,origin:Vertex)->float:
        dy = self.y - origin.y
        dz = self.z - origin.z

        angle = math.degrees(math.atan(dz/dy))

        return angle

    def view_angle_from(self,origin:Vertex)->float:
        dx = self.x - origin.x
        dy = self.y - origin.y

        h = math.hypot(dx,dy)
        angle_rad = math.atan(self.radius/h)

        return math.degrees(angle_rad)

    def __repr__(self):
        return f"Vertex: x:{self.x} y:{self.y} z:{self.z}, {self.vertex_number=}\n"

class HeadingTo:
    def __init__(self, xy_and_yz: tuple[float,float]):
        """
        values between 0 - 360
        where 0 is default
        """
        self.xy_and_yz = xy_and_yz

        self.xy_plane = xy_and_yz[0]
        self.yz_plane = xy_and_yz[1]

        if len(xy_and_yz) > 2:
            raise ValueError(f"vls: {xy_and_yz}: too many values")

    def __repr__(self):
        return f"HeadingTo: {self.xy_plane=} {self.yz_plane}"

class Edge:
    def __init__(self,start:Vertex,end:Vertex, edge_number=None, thickness=1, color=(0,0,0))->None:
        self.start = start
        self.end = end
        self.edge_number = edge_number

        self.thickness = thickness
        self.color = color
    def __repr__(self):
        return f"{self.start=} {self.end=} {self.edge_number=}"
