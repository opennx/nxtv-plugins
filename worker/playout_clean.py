from nx import *
from nx.plugins import WorkerPlugin

__manifest__ = {
    "name"        : "Playout clean",
    "description" : "Deletes media files from playout storage, if they are not needed",
    "author"      : "martas@imm.cz"
}

class Plugin(WorkerPlugin):
    def on_init(self):
        logging.goodnews("{} ({}) initialized".format(__manifest__["name"], __manifest__["description"]))

    def on_main(self):
        logging.debug("I am doing nothing")