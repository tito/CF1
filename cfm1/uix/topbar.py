from kivy.lang import Builder
from kivy.factory import Factory as F

Builder.load_string("""
<CFMToolDropDown@CFMDropDown>:
    CFMButton:
        text: "CLEAR"
        on_press: ctl.tool_clear()
    CFMButton:
        text: "LOAD"
        on_press: ctl.tool_load()
    CFMButton:
        text: "SAVE"
        on_press: ctl.tool_save()
    CFMButton:
        text: "ZOOM"
        on_press: ctl.tool_zoom()
    CFMButton:
        text: "REC OFF"
        on_press: ctl.tool_toggle_rec()

<CFMSequenceDropDown@CFMDropDown>:
    CFMButton:
        text: "LFO"
        on_press: ctl.show_lfo()
    CFMButton:
        text: "ADSR"
        on_press: ctl.show_adsr()

<CFMMenuDropDown@CFMDropDown>:
    CFMButton:
        text: "SONG"
        on_press: ctl.show_song()
    CFMButton:
        text: "PARAM"
        on_press: ctl.show_settings()

<CFMTopbar>:
    CFMIconButton:
        text: chr(ICON_PLAY)
        size_hint_x: None
        width: dp(90)
        on_press: ctl.play()
    CFMIconButton:
        text: chr(ICON_STOP)
        size_hint_x: None
        width: dp(90)
        on_press: ctl.stop()
    CFMToggleButton:
        text: str(model.bpm)
        size_hint_x: None
        width: dp(60)
        state: "down" if (model.encoder_target == "bpm") else "normal"
        on_press: ctl.toggle_bpm()
        group: "encoder"
    CFMToggleButton:
        text: str(model.tracks_length[model.track])
        size_hint_x: None
        width: dp(95)
        state: "down" if (model.encoder_target == "track_length") else "normal"
        on_press: ctl.toggle_track_length()
        group: "encoder"
    CFMButton:
        text: "TOOLS"
        on_press: app.show_dropdown("CFMToolDropDown", self)
        on_release: app.auto_dismiss_dropdown("CFMToolDropDown")
    CFMButton:
        text: "SEQUENCE"
        on_press: app.show_dropdown("CFMSequenceDropDown", self)
        on_release: app.auto_dismiss_dropdown("CFMSequenceDropDown")
    CFMButton:
        text: "MENU"
        on_press: app.show_dropdown("CFMMenuDropDown", self)
        on_release: app.auto_dismiss_dropdown("CFMMenuDropDown")
""")

class CFMTopbar(F.BoxLayout):
    pass