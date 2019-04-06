import cfm1.config as config
from kivy.app import App
from kivy.factory import Factory as F
from kivy.properties import NumericProperty
from kivy.lang import global_idmap
from cfm1.ctl import ctl
from cfm1.model import model

app = None


class CFM1(App):
    def build(self):
        global app
        app = self

        global_idmap["model"] = model
        global_idmap["ctl"] = ctl

        self.bind_keyboard()

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

    def bind_keyboard(self):
        from kivy.core.window import Window

        def on_key_down(window, scancode, *largs):
            if scancode == 117:  # u
                ctl.encoder_changed(1, pressed=False)
                return True
            elif scancode == 105:  # i
                ctl.encoder_changed(-1, pressed=False)
                return True
            elif scancode == 111:  # o
                ctl.encoder_changed(1, pressed=True)
                return True
            elif scancode == 112:  # p
                ctl.encoder_changed(-1, pressed=True)
                return True
            elif scancode == 116:  # t
                model.track = max(0, model.track - 1)
            elif scancode == 121:  # y
                model.track = min(7, model.track + 1)

        Window.bind(on_key_down=on_key_down)


if __name__ == "__main__":
    CFM1().run()