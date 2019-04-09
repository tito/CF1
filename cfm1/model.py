from kivy.properties import (
    NumericProperty, ListProperty, StringProperty)
from kivy.event import EventDispatcher
from cfm1.config import STEPS_MAX, TRACKS_MAX


class CFMModel(EventDispatcher):
    bpm = NumericProperty(120)
    zoom = NumericProperty(4)

    # current selected track
    track = NumericProperty(0)

    # track length
    tracks_length = ListProperty([64] * TRACKS_MAX)

    # [channel 1, 2, ..][step 1, 2, ..][note 1, 2...]
    # note = [note, status, length]
    notes = ListProperty([
        [[] for x in range(STEPS_MAX)]
        for x in range(TRACKS_MAX)])

    # current sequencer range
    xstart = NumericProperty(0)

    # current track y
    ystart = NumericProperty(12 * 3)

    # current encoder target
    encoder_target = StringProperty(None, allownone=True)

    # sequencer step idx
    seq_step_idx = NumericProperty(0)

    # config
    sendinfo = ListProperty([])
    # [Port]
    # [1, 2, 3, 4, 5, 6, 7]
    # 1: Channel
    # 3+4: CV Pitch
    # 4+5: CV Gate
    # 6: Voltage 0-10(5) / -5 to 5(0)
    # 7: Port USB(1) / DIN(2)

    # Syncinfo
    # [1, 2, 3, 4, 5]
    # 1: Midi DYN sync ON(1) / OFF(0)
    # 2: Midi USB sync ON(1) / OFF(0)
    # 3: Clock PPQ 96(6.4) / 48(3.2)
    # 4: Midi USB PPQ 24(1) / 48(2)
    # 5: Midi USB IN(1) / OUT(0)


model = CFMModel()