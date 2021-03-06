import platform

RPI = False
if platform.system() == 'Linux':
    try:
        from RPi import GPIO
        RPI = True
    except:
        pass

CV_ADDRESS = [
    [0x60, 0x50],
    [0x60, 0x52],
    [0x60, 0x54],
    [0x60, 0x56],
    [0x61, 0x50],
    [0x61, 0x52],
    [0x61, 0x54],
    [0x61, 0x56],
    [0x62, 0x50],
    [0x62, 0x52],
    [0x62, 0x54],
    [0x62, 0x56]
]

KEYRANGE = [
    ['C0', 1], ['C#0', 0], ['D0', 1], ['D#0', 0], ['E0', 1], ['F0', 1],
    ['F#0', 0],['G0', 1], ['G#0', 0], ['A0', 1], ['A#0', 0], ['B0', 1],
    ['C1', 1], ['C#1', 0], ['D1', 1], ['D#1', 0], ['E1', 1], ['F1', 1],
    ['F#1', 0],['G1', 1], ['G#1', 0], ['A1', 1], ['A#1', 0], ['B1', 1],
    ['C2', 1], ['C#2', 0], ['D2', 1], ['D#2', 0], ['E2', 1], ['F2', 1],
    ['F#2', 0],['G2', 1], ['G#2', 0], ['A2', 1], ['A#2', 0], ['B2', 1],
    ['C3', 1], ['C#3', 0], ['D3', 1], ['D#3', 0], ['E3', 1], ['F3', 1],
    ['F#3', 0],['G3', 1], ['G#3', 0], ['A3', 1], ['A#3', 0], ['B3', 1],
    ['C4', 1], ['C#4', 0], ['D4', 1], ['D#4', 0], ['E4', 1], ['F4', 1],
    ['F#4', 0],['G4', 1], ['G#4', 0], ['A4', 1], ['A#4', 0], ['B4', 1],
    ['C5', 1], ['C#5', 0], ['D5', 1], ['D#5', 0], ['E5', 1], ['F5', 1],
    ['F#5', 0],['G5', 1], ['G#5', 0], ['A5', 1], ['A#5', 0], ['B5', 1],
    ['C6', 1], ['C#6', 0], ['D6', 1], ['D#6', 0], ['E6', 1], ['F6', 1],
    ['F#6', 0],['G6', 1], ['G#6', 0], ['A6', 1], ['A#6', 0], ['B6', 1],
    ['C7', 1], ['C#7', 0], ['D7', 1], ['D#7', 0], ['E7', 1], ['F7', 1],
    ['F#7', 0],['G7', 1], ['G#7', 0], ['A7', 1], ['A#7', 0], ['B7', 1]]


GPIO_CLK = 21
GPIO_DT = 20
GPIO_SW = 16
GPIO_PWM = 13
GPIO_JACKSTART = 12

SUBDIVISION = 4
MEASURES = 64
STEPS_MAX = MEASURES * SUBDIVISION
TRACKS_MAX = 16

# data index for note
NOTE_PITCH = 0
NOTE_STATUS = 1
NOTE_LENGTH = 2
NOTE_INFO = 3


# load and configure kivy
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
