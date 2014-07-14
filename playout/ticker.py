# -*- coding: utf-8 -*-

from nx import *
from nx.cg import CG
from nx.plugins import PlayoutPlugin


__manifest__ = {
    "name"        : "Ticker",
    "description" : "Ticker with clock",
    "author"      : "martas@imm.cz"
}

class Plugin(PlayoutPlugin):
    def on_init(self):
        self.current_clock = 0
        self.current_tick  = 0

        self.clock_file  = os.path.join(storages[3].get_path(), "media.dir", "cg_clock.png")
        self.ticker_file = os.path.join(storages[3].get_path(), "media.dir", "cg_ticker.png")

    def on_change(self):
        if self.channel.current_asset: #Set your condition here (e.g. 'commercial' etc.)
            self.tasks = [self.show]
        else:
            self.tasks = []
            self.hide()

    def show(self):
        now = time.time()
        nowc = time.strftime("%H:%M")
        if nowc != self.current_clock:
            self.current_clock = nowc
            cg = CG()
            cg.clock(nowc)
            cg.save(self.clock_file)
            self.query("PLAY {} cg_clock".format(self.layer(99)))

#        if now - self.current_tick > 10:
#            self.current_tick = now
#            cg = CG()
#            cg.ticker("Ticker z {}".format(now))
#            cg.save(self.ticker_file)
#            self.query("PLAY {} cg_ticker".format(self.layer(98)))

        return False

    def hide(self):
        self.query("CLEAR {}".format(self.layer(99)))
        self.query("CLEAR {}".format(self.layer(98)))
