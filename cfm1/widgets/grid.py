from kivy.lang import Builder
from kivy.factory import Factory as F
from kivy.properties import NumericProperty, ListProperty
from kivy.graphics import (
    Color, Mesh, RenderContext, PushMatrix,
    PopMatrix, Translate)
from kivy.clock import Clock
import numpy as np


FS = """
$HEADER$

void main(void) {
    gl_FragColor = frag_color * texture2D(texture0, tex_coord0);
}
"""

VS = """
$HEADER$
attribute vec4 vColor;
void main(void) {
    frag_color = vColor * color * vec4(1.0, 1.0, 1.0, opacity);
    tex_coord0 = vTexCoords0;
    gl_Position = projection_mat * modelview_mat * vec4(vPosition.xy, 0.0, 1.0);
}
"""


class Grid(F.Widget):
    cols = NumericProperty(16)
    rows = NumericProperty(8)
    spacing = NumericProperty("2dp")
    sqcolor = ListProperty([0.2, 0.2, 0.2, 1.])
    sqsize = NumericProperty(10)

    def __init__(self, **kwargs):
        self.canvas = RenderContext(
            use_parent_projection=True,
            use_parent_modelview=True,
            fs=FS, vs=VS
        )
        self.sync_vertices = Clock.create_trigger(
            self._sync_vertices, -1)
        super(Grid, self).__init__(**kwargs)

    def on_size(self, _, size):
        self.build_grid()

    def on_pos(self, _, pos):
        if not hasattr(self, "g_translate"):
            return
        self.g_translate.x = self.x
        self.g_translate.y = self.y

    def build_grid(self):
        vertices = []
        indices = []

        # ideal widget size according to cols/rows
        nw = int(self.width / self.cols)
        nh = int(self.height / self.rows)
        self.sqsize = sqsize = min(nw, nh)

        nrows = float(self.rows)
        ncols = float(self.cols)
        s = self.spacing / 2.
        i = 0
        r, g, b, a = self.sqcolor
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * sqsize
                y = row * sqsize
                # (vPosition + vTexCoords0 + vColor) * 4
                vertices += [
                    x + s, y + s,
                    0, 0,
                    r, g, b, a,
                    x + sqsize - s, y + s,
                    1, 0,
                    r, g, b, a,
                    x + sqsize - s, y - s + sqsize,
                    1, 1,
                    r, g, b, a,
                    x + s, y - s + sqsize,
                    0, 1,
                    r, g, b, a,
                ]
                indices += [
                    i, i + 2, i + 1,
                    i, i + 3, i + 2
                ]
                i += 4

        self.vertices = vertices = np.array(vertices, dtype="float32")
        self.vertices_sh = self.vertices.reshape(
            (self.cols * self.rows, 4, 8)
        )

        if hasattr(self, "g_mesh"):
            self.g_mesh.vertices = vertices
            self.g_mesh.indices = indices
        else:
            vertex_format = (
                (b"vPosition", 2, "float"),
                (b"vTexCoords0", 2, "float"),
                (b"vColor", 4, "float")
            )

            with self.canvas:
                Color(1., 1., 1., 1.)
                PushMatrix()
                self.g_translate = Translate(self.x, self.y, 1.)
                self.g_mesh = Mesh(
                    vertices=vertices,
                    indices=indices,
                    mode="triangles",
                    fmt=vertex_format
                )
                PopMatrix()

    def _sync_vertices(self, *largs):
        self.g_mesh.vertices = self.vertices

    def set_color(self, ix, iy, color):
        v = self.vertices_sh
        i0 = ix + (iy * self.cols)
        v[i0, :, -4:] = color
        self.sync_vertices()

    def get_coords_at(self, x, y):
        sqsize = float(self.sqsize)
        ix = int((x - self.x) / sqsize)
        iy = int((y - self.y) / sqsize)
        return ix, iy

    def on_grid_down(self, ix, iy):
        return {}

    def on_grid_move(self, ix, iy, data):
        return

    def on_grid_up(self, ix, iy, data):
        return

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        touch.grab(self)
        ix, iy = self.get_coords_at(*touch.pos)
        data = self.on_grid_down(ix, iy)
        touch.ud["grid_data"] = data
        return True

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if touch.grab_current is not self:
            return
        data = touch.ud["grid_data"]
        ix, iy = self.get_coords_at(*touch.pos)
        self.on_grid_move(ix, iy, data)
        return True

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        data = touch.ud["grid_data"]
        ix, iy = self.get_coords_at(*touch.pos)
        self.on_grid_up(ix, iy, data)
        return True


if __name__ == "__main__":
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    grid = Grid(size=Window.size)
    grid.set_color(0, 0, (0.25, 0.25, 0.25, 1.))
    grid.set_color(1, 1, (1, 0.25, 0.25, 1.))
    runTouchApp(grid)