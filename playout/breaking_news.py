import time

from nxcg import CG
from nx.plugins import PlayoutPlugin, PlayoutPluginSlot as Slot

__manifest__ = {
    "name"        : "breaking_news",
    "description" : "Breaking news plugin",
    "author"      : "martas@imm.cz"
}

class Plugin(PlayoutPlugin):
    def on_init(self):
        self.id_layer = 89
        self.show_time = 0
        self.add_slot("text", title="Text")
        self.add_slot("button", title="Show", action=self.show)
        self.add_slot("button", title="Hide", action=self.hide)

    def show(self):
        text = self.slot_value(0)
        if not text:
            self.clear()
            return

        cg = CG()
        cg.text_area("Breaking news", text)
        cg.save("/mnt/nxtv_03/media.dir/cg_breaking_news.png")

        self.show_time = time.time()
        self.tasks = [self.auto_hide]


        self.query("PLAY {} cg_breaking_news PUSH 15 RIGHT".format(self.layer(), self.slot_value(0)))

    def hide(self):
        self.query("PLAY {} BLANK PUSH 15 LEFT".format(self.layer()))

    def auto_hide(self):
        if self.show_time < time.time() - 10:
            self.query("PLAY {} BLANK PUSH 15 LEFT".format(self.layer()))
            return True
        return False
