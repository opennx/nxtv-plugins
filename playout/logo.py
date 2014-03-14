from nx.plugins import PlayoutPlugin

__manifest__ = {
    "name"        : "Logo",
    "description" : "Simple channel identification",
    "author"      : "martas@imm.cz"
}

class Plugin(PlayoutPlugin):
    def on_init(self):
        self.id_layer = 100

    def on_change(self):
        if self.channel.current_asset: #Set your condition here (e.g. 'commercial' etc.)
            self.show()
        else:
            self.hide()

    def show(self):
        self.query("PLAY {} static_logo".format(self.layer()))

    def hide(self):
        self.query("CLEAR {}".format(self.layer()))
