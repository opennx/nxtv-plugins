# -*- coding: utf-8 -*-

from nx import *
from nxcg import CG
from nx.plugins import PlayoutPlugin

__manifest__ = {
    "name"        : "Music label",
    "description" : "Zobrazuje, jak se jmenuje písnička",
    "author"      : "martas@imm.cz"
}

class Plugin(PlayoutPlugin):
    def on_init(self):
        self.id_layer = 12
        self.image_file = os.path.join(storages[3].local_path, "media.dir", "cg_music_label.png")


    def on_change(self):
        if self.channel.current_asset["id_folder"] == 5 and not self.channel.current_asset["contains/cg_text"]:
            cg = CG()
            cg.music_label(self.channel.current_asset["title"], self.channel.current_asset["role/performer"])
            cg.save(self.image_file)
            self.tasks = [self.begin_show, self.begin_hide, self.end_show, self.end_hide]
        else:
            self.tasks = []
            self.query("CLEAR {}".format(self.layer()))


    def begin_show(self):
        if self.channel.get_position() < 10:
            return False
        self.query("PLAY {} cg_music_label PUSH 15 RIGHT".format(self.layer()))
        return True


    def begin_hide(self):
        if self.channel.get_position() < 200:
            return False
        self.query("PLAY {} blank PUSH 15 LEFT".format(self.layer()))
        return True


    def end_show(self):
        if self.channel.get_position() < self.channel.get_duration() - 300:
            return False
        self.query("PLAY {} cg_music_label PUSH 15 RIGHT".format(self.layer()))
        return True


    def end_hide(self):
        if self.channel.get_position() < self.channel.get_duration() - 100:
            return False
        self.query("PLAY {} blank PUSH 15 LEFT".format(self.layer()))
        return True

