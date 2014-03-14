# -*- coding: utf-8 -*-

from nx import *
from nx.cg import CG
from nx.plugins import PlayoutPlugin


__manifest__ = {
    "name"        : "Templates",
    "description" : "Zobrazuje, na co nového zase vědci přišli, zprávy, počasí a další píčoviny",
    "author"      : "martas@imm.cz"
}

class Plugin(PlayoutPlugin):
    def on_init(self):
        self.id_layer = 11
        self.image_file = os.path.join(storages[3].get_path(), "media.dir", "cg_vedci_zjistili.png")

        self.templates = {
            1272 : [self.vedci_show, self.vedci_hide], # Vedci zjistili
        }


    def on_change(self):
        id_asset = self.channel.current_asset.id
        self.tasks = self.templates.get(id_asset, [])
        if not self.tasks:
            self.query("CLEAR {}".format(self.layer()))





    def vedci_show(self):
        cg = CG()
        cg.vedci_zjistili()
        cg.save(self.image_file)
        self.query("PLAY {} cg_vedci_zjistili WIPE 15 RIGHT".format(self.layer()))
        return True

    def vedci_hide(self):
        if self.channel.get_position() < 230: 
            return False
        self.query("PLAY {} blank MIX 15 ".format(self.layer()))
        return True


