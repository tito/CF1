import cfm1.config as config
from kivy.app import App
from kivy.factory import Factory as F
from kivy.properties import NumericProperty
from kivy.lang import global_idmap

app = None


class CFM1(App):
    bpm = NumericProperty(120)

    def build(self):
        global app
        app = self

        from cfm1.ctl import controller
        from cfm1.model import model

        global_idmap["model"] = model
        global_idmap["ctl"] = controller

        from cfm1.uix.ui import CFMUI
        return CFMUI()

    def show_dropdown(self, name, wid):
        if hasattr(self, name):
            dropdown = getattr(self, name)
        else:
            dropdown = F.get(name)()
            setattr(self, name, dropdown)
        dropdown.auto_dismiss = False
        dropdown.open(wid)

    def auto_dismiss_dropdown(self, name):
        if not hasattr(self, name):
            return
        dropdown = getattr(self, name)
        dropdown.auto_dismiss = True


if __name__ == "__main__":
    CFM1().run()