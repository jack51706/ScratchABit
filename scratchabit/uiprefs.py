from picotui.widgets import *
from picotui.dialogs import add_ok_cancel_buttons
from .utils import bidict


class DPreferences(Dialog):

    OPT_MAP = bidict({0: "asm", 1: "pseudoc", 2: "pseudoc+asm"})

    def __init__(self):
                super().__init__(10, 5, 40, 7, title="Preferences")
                self.add(2, 2, "Listing:")
                self.listing = WDropDown(15, ["Asm", "PseudoC", "PseudoC + Asm"])
                self.add(11, 2, self.listing)
                self.add(2, 3, "(PseudoC support depends on CPU plugin)")
                self.autosize(1, 0)
                add_ok_cancel_buttons(self)

    def set_listing(self, val):
        self.listing.choice = self.OPT_MAP[val]

    def result(self):
                res = self.loop()
                if res == ACTION_CANCEL:
                    return res
                return {
                    "listing": self.OPT_MAP[self.listing.choice],
                }


def handle(app):
    d = DPreferences()
    d.set_listing(app.cpu_plugin.mnem_type)
    res = d.result()
    if res == ACTION_CANCEL:
        app.main_screen.e.redraw()
        return
    app.cpu_plugin.mnem_type = res["listing"]
    app.cpu_plugin.config()
    app.main_screen.e.update_model()
