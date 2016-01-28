# -*- coding: utf-8 -*-

import urllib2

from nx import *
from nxcg import CG
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

        self.clock_file  = os.path.join(storages[3].local_path, "media.dir", "cg_clock.png")
        self.ticker_file = os.path.join(storages[3].local_path, "media.dir", "cg_ticker.png")

    def on_change(self):
        if self.channel.current_asset["id_folder"] == 5:
            self.current_clock = 0
            self.current_tick = 0
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

        if now - self.current_tick > 10:
            try:
                data = json.loads(urllib2.urlopen("http://localhost:42200", timeout=1).read())
            except:
                data = False

            if data:
                self.current_tick = now
                cg = CG()
                cg.ticker(data["title"])
                cg.save(self.ticker_file)
                self.query("PLAY {} cg_ticker MIX 10".format(self.layer(98)))

        return False

    def hide(self):
        self.query("CLEAR {}".format(self.layer(99)))
        self.query("CLEAR {}".format(self.layer(98)))
