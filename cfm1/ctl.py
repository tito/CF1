from cfm1.model import model
from cfm1.config import (
    STEPS_MAX, KEYRANGE,
    NOTE_PITCH, NOTE_STATUS, NOTE_LENGTH, NOTE_INFO)
from cfm1.service import service


class CFMController(object):
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

    def set_bpm(self, bpm):
        model.bpm = bpm
        service.sock_seq.send_json(("BPM", bpm))

    def set_track_length(self, track, length):
        model.tracks_length[track] = length
        service.sock_seq.send_json(("TRACK_LENGTH", track, length))

    def set_note_length(self, note, length):
        if note[NOTE_LENGTH] == length:
            return
        note[NOTE_LENGTH] = length
        service.sock_seq.send_json(("NOTEUPD", note))

    def add_note(self, note):
        service.sock_seq.send_json(("NOTEADD", note))

    def remove_note(self, note):
        service.sock_seq.send_json(("NOTEDEL", note))

    def create_note_from_grid(self, ix, iy):
        track = self.get_current_track()
        step = model.xstart + ix
        # note = pitch, state, length, (track, step)
        note = [iy + model.ystart, None, 1, (model.track, step)]
        track[step].append(note)
        self.add_note(note)
        return note

    def get_note_from_grid(self, ix, iy):
        track = self.get_current_track()
        step = model.xstart + ix
        iy += model.ystart
        for note in track[step]:
            if note[0] == iy:
                return note

    def remove_note_from_grid(self, ix, note):
        track = self.get_current_track()
        step = model.xstart + ix
        if note in track[step]:
            track[step].remove(note)
            self.remove_note(note)
            return True

    #
    # encoder button
    #

    def encoder_changed(self, direction, pressed=False):
        if model.encoder_target == "bpm":
            self.set_bpm(max(40, min(300, model.bpm + direction)))
        elif model.encoder_target == "track_length":
            length = model.tracks_length[model.track]
            length = max(1, min(STEPS_MAX, length + direction))
            self.set_track_length(model.track, length)
        else:
            if not pressed:
                model.xstart = max(0, min(STEPS_MAX, model.xstart + direction))
            else:
                model.ystart = max(0, min(len(KEYRANGE), model.ystart + direction))


ctl = CFMController()