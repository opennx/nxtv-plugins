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
        self.clock_file  = os.path.join(storages[3].local_path, "media.dir", "cg_clock.png")
        self.ticker_file = os.path.join(storages[3].local_path, "media.dir", "cg_ticker.png")
        self.ignore_guid = []
        self.ticker_start()


    def ticker_start(self):
        self.current_clock = 0
        self.current_tick  = 0
        self.tasks = [self.show]


    def on_change(self):
        self.ticker_start()

    def show(self):
        now = time.time()
        nowc = time.strftime("%H:%M")
        if nowc != self.current_clock:
            self.current_clock = nowc
            cg = CG()
            cg.clock(nowc)
            cg.save(self.clock_file)
            self.query("PLAY {} cg_clock".format(self.layer(99)))

        if now - self.current_tick > 8:
            try:
                data = json.loads(urllib2.urlopen("http://localhost:42200", timeout=1).read())
            except:
                data = False

            if data:
                if data["identifier/guid"] in self.ignore_guid:
                    return False

                cg = CG()
                if not cg.ticker(data["title"]):
                    logging.debug("Ticker message {} is too long. skipping".format(data["title"]))
                    self.ignore_guid.append(data["identifier/guid"])
                    return False

                cg.save(self.ticker_file)
                self.current_tick = now
                self.query("PLAY {} cg_ticker MIX 5".format(self.layer(98)))

        return False

    def hide(self):
        self.query("CLEAR {}".format(self.layer(99)))
        self.query("CLEAR {}".format(self.layer(98)))
