from cfm1.model import model
from cfm1.config import STEPS_MAX, KEYRANGE

class CFMController(object):
    model = None

    def play(self):
        pass

    def stop(self):
        pass

    def toggle_bpm(self):
        if model.encoder_target != "bpm":
            model.encoder_target = "bpm"
        else:
            model.encoder_target = None

    def toggle_track_length(self):
        if model.encoder_target != "track_length":
            model.encoder_target = "track_length"
        else:
            model.encoder_target = None

    def tool_clear(self):
        pass

    def tool_load(self):
        pass

    def tool_save(self):
        pass

    def tool_zoom(self):
        pass

    def tool_toggle_rec(self):
        pass

    def show_lfo(self):
        pass

    def show_adsr(self):
        pass

    def show_song(self):
        pass

    def show_settings(self):
        pass

    # track
    def get_current_track(self):
        return model.notes[model.track]

    def create_note_from_grid(self, ix, iy, track=None):
        if track is None:
            track = self.get_current_track()
        note = [iy + model.ystart, None, 1]
        step = model.xstart + ix
        track[step].append(note)
        return note

    def get_note_from_grid(self, ix, iy, track=None):
        if track is None:
            track = self.get_current_track()
        step = model.xstart + ix
        iy += model.ystart
        for note in track[step]:
            if note[0] == iy:
                return note

    def remove_note_from_grid(self, ix, note, track=None):
        if track is None:
            track = self.get_current_track()
        step = model.xstart + ix
        if note in track[step]:
            track[step].remove(note)
            return True

    #
    # encoder button
    #
    def encoder_changed(self, direction, pressed=False):
        if model.encoder_target == "bpm":
            model.bpm = max(40, min(300, model.bpm + direction))
        elif model.encoder_target == "track_length":
            pass
        else:
            if not pressed:
                model.xstart = max(0, min(STEPS_MAX, model.xstart + direction))
            else:
                model.ystart = max(0, min(len(KEYRANGE), model.ystart + direction))

ctl = CFMController()