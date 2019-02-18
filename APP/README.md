CFM1 App

-----
Installation

- Install [Kivy](https://kivy.org/#download) for python 3
- Install alsa headers (for example on ubuntu: ``sudo apt install libasound2-dev``)

Kivy's installation in a virtualenv is a little painful.
If you mastered it, you can install CFM1 python deps listed in ``requirements.txt`` in your virtualenv.

Otherwise, you can follow these steps:
- Install pip (for example on ubuntu: ``sudo apt install python3-pip``)
- Install CFM1 python deps: ``sudo pip3 install -r requirements.txt``

Then, hopefully, launch CFM1 with:
- ``python3 cf1c.py``

Note: you can do the same with python 2 (replace with ``python-pip``, ``pip`` and ``python`` accordingly)
