from kivy.properties import (
    NumericProperty, ListProperty, StringProperty)
from kivy.event import EventDispatcher
from cfm1.config import STEPS_MAX


class CFMModel(EventDispatcher):
    bpm = NumericProperty(120)
    zoom = NumericProperty(4)

    # current selected track
    track = NumericProperty(0)

    # [channel 1, 2, ..][step 1, 2, ..][note 1, 2...]
    # note = [note, status, length]
    notes = ListProperty([
        [[] for x in range(STEPS_MAX)]
        for x in range(8)])

    # current sequencer range
    xstart = NumericProperty(0)

    # current track y
    ystart = NumericProperty(12 * 3)

    # current encoder target
    encoder_target = StringProperty(None, allownone=True)


model = CFMModel()