from turtledemo.penrose import draw

from Faces import Vertex, HeadingTo
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
        self.field_of_view = 100  # degrees

        self.render_out_format = (800, 600)

        self.from_focal_point = (self.render_out_format[0] / 2) / (math.tan(math.radians(self.field_of_view / 2)))
        print(f"{self.from_focal_point=}")

    def update_position(self, pos: Vertex, heading: HeadingTo) -> None:
        self.pos = pos
        self.heading = heading

    def render_from_top(self, scene: Scene) -> None:
        canvas_from_top = Img()

        canvas_from_top.draw_camera(pos=self.pos, heading=self.heading,fov=self.field_of_view)

        for point in scene.vertexes:
            print(point)
            canvas_from_top.draw_point_at_coordinate(point=point, vertex_type="vtx")

        canvas_from_top.show()

    def render_vertex(self, scene: Scene) -> None:
        canvas = Img(self.render_out_format)

        for draw_vertex in scene.vertexes:
            x_proportion = draw_vertex
