from kivy.lang import Builder
from kivy.factory import Factory as F

Builder.load_string("""
#:import CFMTopbar cfm1.uix.topbar
#:import CFMSequencer cfm1.uix.sequencer
<CFMUI>:
    cols: 1
    CFMTopbar:
        size_hint_y: None
        height: dp(60)
    CFMSequencer
""")

class CFMUI(F.GridLayout):
    pass