from Faces import Vertex, HeadingTo, Edge, Face
from Scene import Scene

from PIL import Image, ImageDraw
import math


class Img:
    vertex_types = {  # color, radius
        "cam": ((255, 0, 0), 10),
        "vtx": ((0, 0, 255), 8)
    }

    def __init__(self, size=(800, 800)):
        self.size = size
        self.img = Image.new("RGB", size, "white")
        self.draw = ImageDraw.Draw(self.img)

        # end lines in a circle around origin with r=hyp(corners)
        self.distance_from_middle_to_corner = math.hypot(self.size[0], self.size[1]) / 2

        self.fit_vertexes_across = 10  # -10 0 10
        self.image_multiplier = (size[0] / (2 * self.fit_vertexes_across),
                                 size[1] / (2 * self.fit_vertexes_across))

    def from_coords_to_pixels(self, point: Vertex) -> tuple[float, float]:
        x_on_image = (point.x + self.fit_vertexes_across) * self.image_multiplier[0]  # so min is at 0 and max at 2fit
        # y needs to be mirrored
        y_on_image = self.size[1] - (point.y + self.fit_vertexes_across) * self.image_multiplier[
            1]  # so min is at 0 and max at 2fit

        return x_on_image, y_on_image

    def draw_point_at_coordinate(self, point: Vertex, vertex_type: str) -> None:
        if vertex_type not in Img.vertex_types.keys():
            raise KeyError(f"vertex type: {vertex_type=} not found in Img.vertex_types")

        col, radius = Img.vertex_types[vertex_type]
        x, y = self.from_coords_to_pixels(point)

        self.draw.circle((x, y), radius, col)

    def draw_line_vertex_a_angle(self, origin: Vertex, angle: float):
        origin_pixels = self.from_coords_to_pixels(origin)

        end_x = math.sin(math.radians(angle)) * self.distance_from_middle_to_corner
        end_y = -math.cos(math.radians(angle)) * self.distance_from_middle_to_corner

        end_x+=origin_pixels[0]
        end_y+=origin_pixels[1]

        self.draw.line((origin_pixels[0], origin_pixels[1], end_x, end_y), (0, 0, 0), 2)

    def draw_camera(self, pos: Vertex, heading: HeadingTo,fov:float):
        # draw the point
        self.draw_point_at_coordinate(point=pos, vertex_type="cam")
        # draw the heading line
        #self.draw_line_vertex_a_angle(origin=pos, angle=heading.xy_plane)
        # draw the view angle
        self.draw_line_vertex_a_angle(origin=pos, angle=heading.xy_plane - (fov / 2))
        self.draw_line_vertex_a_angle(origin=pos, angle=heading.xy_plane + (fov / 2))

    def show(self):
        self.img.show()


class Cam:
    def __init__(self, pos: Vertex, heading: HeadingTo):
        self.pos = pos
        self.heading = heading
        self.field_of_view = 120  # degrees
        self.render_out_format = (800, 608)

        self.frames = []

        self.from_focal_point = (self.render_out_format[0] / 2) / (math.tan(math.radians(self.field_of_view / 2)))
        print(f"{self.from_focal_point=}")
        # clac based on fov and output
        self.field_of_view_yz = math.degrees(math.atan((self.render_out_format[1]/2)/self.from_focal_point))
        print(f"{self.field_of_view_yz=}")

    def update_position(self, pos: Vertex, heading: HeadingTo) -> None:
        self.pos = pos
        self.heading = heading

    def render_from_top(self, scene: Scene) -> None:
        canvas_from_top = Img()

        canvas_from_top.draw_camera(pos=self.pos, heading=self.heading,fov=self.field_of_view)

        for point in scene.objects.values():
            if type(point) is Vertex:
                canvas_from_top.draw_point_at_coordinate(point=Vertex(point.mid_point), vertex_type="vtx")

        canvas_from_top.show()

    def angle_to_pixels(self,angle:float)->float:
        return self.from_focal_point * math.tan(math.radians(angle))

    def center_to_relative(self,x:float, y:float)->tuple[float,float]:
        return x + (self.render_out_format[0] / 2), (self.render_out_format[1] / 2) - y

    def relative_vertex_pos(self,draw_vertex:Vertex)->tuple[float,float,float]:
        """x, y, view field (in pixels, but not centered)"""
        relative_angle_xy = draw_vertex.global_angle_to_xy(origin=self.pos) - self.heading.xy_plane
        x_pixels_pos = self.angle_to_pixels(relative_angle_xy)

        relative_angle_yz = draw_vertex.global_angle_to_yz(origin=self.pos) - self.heading.yz_plane
        y_pixels_pos = self.angle_to_pixels(relative_angle_yz)

        view_angle = draw_vertex.view_angle_from(origin=self.pos)
        radius = self.angle_to_pixels(view_angle)

        return x_pixels_pos,y_pixels_pos,radius

    def render_front(self, scene: Scene) -> None:
        canvas = Img(self.render_out_format)
        scene.sort_objects_by_distance(self.pos)

        # draw all vertexes
        for render_object in scene.objects.values():

            if isinstance(render_object, Vertex):

                x, y, radius = self.relative_vertex_pos(render_object)
                canvas.draw.circle(self.center_to_relative(x, y), radius, render_object.color)

            elif isinstance(render_object, Edge):
                start_x, start_y, _ = self.relative_vertex_pos(render_object.start)
                start_x, start_y = self.center_to_relative(start_x, start_y)

                end_x,end_y,_ = self.relative_vertex_pos(render_object.end)
                end_x, end_y = self.center_to_relative(end_x,end_y)

                canvas.draw.line((start_x,start_y,end_x,end_y),fill=render_object.color,width=render_object.thickness)

            elif isinstance(render_object, Face):
                real_cords = []

                for vertex in render_object.vertexes:
                    real_cords.append(self.center_to_relative(*self.relative_vertex_pos(vertex)[0:2]))

                print(real_cords)

                canvas.draw.polygon(real_cords,render_object.color)


        canvas.show()

        self.frames.append(canvas.img)