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

GPIO_CLK = 21
GPIO_DT = 20
GPIO_SW = 16
GPIO_PWM = 13
GPIO_JACKSTART = 12

# load and configure kivy
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
