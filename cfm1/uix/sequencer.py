from kivy.lang import Builder
from kivy.factory import Factory as F
from cfm1.widgets.grid import Grid
from cfm1.ctl import ctl
from cfm1.model import model
from cfm1.config import KEYRANGE

Builder.load_string("""
<CFMSequencerNoteRangeButton@CFMGenericButton>:
    odd: False
    background_color: (0.2, 0.2, 0.2, 1) if root.odd else (1, 1, 1, 1)

<CFMSequencerNoteRange>:
    cols: 1
    spacing: 2
    padding: 1

<CFMSequencer>:
    rows: 1
    CFMSequencerNoteRange:
        size_hint: None, None
        width: dp(40)
        height: seq.sqsize * 8
    CFMSequencerGrid:
        id: seq
""")

COLOR_ACTIVE = (1., 1., 1., 1.)
COLOR_DEFAULT = (0.2, 0.2, 0.2, 1.)
COLOR_NOTE_LENGTH = (0.5, 0.5, 0.5, 1.)


class CFMSequencerNoteRange(F.GridLayout):
    def __init__(self, **kwargs):
        super(CFMSequencerNoteRange, self).__init__(**kwargs)
        model.bind(ystart=self.populate)
        self.populate()

    def populate(self, *largs):
        F.CFMSequencerNoteRangeButton()
        self.clear_widgets()
        for y in reversed(range(8)):
            iy = y + model.ystart
            key = KEYRANGE[iy]
            btn = F.CFMSequencerNoteRangeButton(
                text=key[0], odd=not key[1])
            self.add_widget(btn)


class CFMSequencerGrid(Grid):
    def on_grid_down(self, ix, iy):
        data = {"iy": iy, "ix": ix}
        note = ctl.get_note_from_grid(ix, iy)
        if note:
            ctl.remove_note_from_grid(ix, note)
        else:
            note = ctl.create_note_from_grid(ix, iy)
        data["note"] = note
        self._refresh_grid(iy)
        return data

    def on_grid_move(self, ix, iy, data):
        if not data["note"]:
            return
        if data["iy"] != iy:
            return
        note = data["note"]
        note[2] = max(1, ix - data["ix"] + 1)
        self._refresh_grid(iy)

    def on_grid_up(self, ix, iy, data):
        if not data["note"]:
            return
        if data["iy"] != iy:
            return

    def _refresh_grid(self, iy):
        track = ctl.get_current_track()
        notelength = 0
        for ix in range(16):
            step = model.xstart + ix
            notey = model.ystart + iy
            notes = track[step]

            if notelength > 0:
                color = COLOR_NOTE_LENGTH
                notelength -= 1
            else:
                color = COLOR_DEFAULT
            for note in notes:
                if note[0] == notey:
                    color = COLOR_ACTIVE
                    notelength = max(notelength, note[2] - 1)
            self.set_color(ix, iy, color)


class CFMSequencer(F.GridLayout):
    pass