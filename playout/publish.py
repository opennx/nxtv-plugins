import json
from urllib2 import urlopen

from nx import *
from nx.plugins import PlayoutPlugin

__manifest__ = {
    "name"        : "Publish",
    "description" : "Pushs playout state information to web site",
    "author"      : "martas@imm.cz"
}

class Plugin(PlayoutPlugin):
    def on_init(self):
        self.data = {}
        self.last_run = 0
        self.url = config.get("publish_url", False)
        
    def on_change(self):
        if not self.url:
            return

        self.data = {}
        if not self.channel.current_asset:
            logging.warning("Publisher: No current asset")
            return 

        if not self.channel.current_event:
            logging.warning("Publisher: No current event")
            return

        asset = self.channel.current_asset
        event = self.channel.current_event

        if asset["id_folder"] == 5:
            self.data["title"] = asset["title"]
            self.data["subtitle"] = asset["role/performer"]
            if event["id_asset"]:
                self.data["description"] = asset["description"]
            else:
                # music blocks can show block description instead asset's
                self.data["description"] = asset["description"] or event["description"]
        else:
            self.data["title"] = event["title"]
            self.data["description"] = event["description"]

        url = False
        if asset["source/url"]:
            url = asset["source/url"]
        elif asset["identifier/youtube"]:
            url = "https://www.youtube.com/watch?v={}".format(asset["identifier/youtube"])
        elif asset["identifier/vimeo"]:
            url = "http://vimeo.com/{}".format(asset["identifier/vimeo"])

        meta = []
        self.data["meta"] = meta
        self.data["id_asset"] = self.channel.current_asset.id
        if url:
            self.data["url"] = url

    def on_main(self):
        if not self.url:
            return

        if time.time() - self.last_run > 5 and self.channel.current_asset:
            self.publish()
            self.last_run = time.time()

    def publish(self):
        post_data = json.dumps(self.data)
        try:
            urlopen(self.url, post_data.encode("ascii"), timeout=1)
        except:
            logging.warning("Publisher: Timeout")