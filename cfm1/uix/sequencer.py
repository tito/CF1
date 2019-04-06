from kivy.lang import Builder
from kivy.factory import Factory as F
from cfm1.widgets.grid import Grid

Builder.load_string("""
<CFMSequencer>:
    rows: 1
    CFMSequencerGrid
""")

ACTIVE_COLOR = (1., 1., 1., 1.)

class CFMSequencerGrid(Grid):
    def on_grid_down(self, ix, iy):
        self.set_color(ix, iy, ACTIVE_COLOR)

    def on_grid_move(self, ix, iy, data):
        self.set_color(ix, iy, ACTIVE_COLOR)

    def on_grid_up(self, ix, iy, data):
        self.set_color(ix, iy, ACTIVE_COLOR)


class CFMSequencer(F.GridLayout):
    pass