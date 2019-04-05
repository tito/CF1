from kivy.properties import NumericProperty
from kivy.event import EventDispatcher


class CFMModel(EventDispatcher):
    bpm = NumericProperty(120)


model = CFMModel()