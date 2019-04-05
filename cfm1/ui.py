from kivy.lang import Builder
from kivy.factory import Factory as F

Builder.load_string("""
#:import CFMTopbar cfm1.uix.topbar
<CFMUI>:
    cols: 1
    CFMTopbar:
        size_hint_y: None
        height: dp(60)
    Widget
""")

class CFMUI(F.GridLayout):
    pass