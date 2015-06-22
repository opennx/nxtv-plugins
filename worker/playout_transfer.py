from nx import *
from nx.objects import *
from nx.jobs import send_to
from nx.plugins import WorkerPlugin

__manifest__ = {
    "name"        : "Playout transfer",
    "description" : "Automatically transfers media to playout storage before broadcast",
    "author"      : "martas@imm.cz"
}



def scheduled_assets(id_channel, db=False):
    db = db or DB()  
    start = time.time()
    stop  = start + (3600*24)
    db.query("SELECT DISTINCT(i.id_asset) FROM nx_events as e, nx_items as i WHERE e.id_channel = %s AND e.start > %s and e.start < %s AND i.id_bin = e.id_magic AND i.id_asset > 0", [id_channel, start, stop])
    for id_asset, in db.fetchall():
        yield id_asset 


class Plugin(WorkerPlugin):
    def on_init(self):
        logging.goodnews("{} ({}) initialized".format(__manifest__["name"], __manifest__["description"]))

    def on_main(self):
        for id_channel in config["playout_channels"]:
            channel_cfg = config["playout_channels"][id_channel]

            db = DB()
            for id_master in scheduled_assets(id_channel, db=db):
                master_asset = Asset(id_master, db=db)

                if master_asset["status"] != ONLINE:
                    continue

                if not master_asset["audio/r128/i"]:
                    continue

                id_playout = master_asset[channel_cfg["playout_spec"]]

                transfer = False
                
                if not id_playout:
                    transfer = True
                
                else:
                    playout_asset = Asset(id_playout)
                    if not os.path.exists(playout_asset.file_path):
                        transfer = True

                if transfer:
                    send_to(id_master, channel_cfg["send_action"], restart_existing=True, db=db)

