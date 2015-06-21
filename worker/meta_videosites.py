from nx import *
from nx.plugins import WorkerPlugin
from nx.objects import Asset

import traceback
import urllib2
import re

__manifest__ = {
    "name"        : "SiteMeta",
    "description" : "Obtains video metadata from various (so far youtube and vimeo) video sites",
    "author"      : "martas@imm.cz"
}



def youtubedata(ytid):
    result = {}

    url = "https://www.youtube.com/watch?v={}".format(ytid)
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    data = urllib2.urlopen(req).read()

    exps = {
        "title" : r"<title[^>]*>([^<]+)</title>",
        "title/original" : r"<title[^>]*>([^<]+)</title>",
        "subject" : r"<meta name\=\"keywords\" content\=\"([^<]+)\">",
        "description" : r"<meta name\=\"description\" content\=\"([^<]+)\">",
        "description/original" : r"<meta name\=\"description\" content\=\"([^<]+)\">",
    }

    for key in exps:
        exp = exps[key]
        m = re.findall(exp, data)
        result[key] = m[0]

    if data.find("/t/creative_commons") > -1:
        result["rights"] = "CC BY 3.0"
    else:
        result["rights"] = "Youtube proprietary"

    if not "google_api_key" in config:
        return result

    parts = [
        "snippet",
        "contentDetails",
        "statistics",
        "status",
        "topicDetails"
        ]

    URL = "https://www.googleapis.com/youtube/v3/videos?id={}&key={}&part={}".format(
            ytid,
            config["google_api_key"],
            ",".join(parts)
            )

    dump = urllib2.urlopen(URL).read()
    dump = json.loads(dump)

    item = dump["items"][0]
    title = item["snippet"]["title"],
    description = item["snippet"]["description"],

    result["title"] = result["title/original"] = title[0]
    result["description"] = result["description/original"] = description[0]

    if item["status"]["license"] == "creativeCommon":
        result["rights"] = "CC BY 3.0"
    else:
        result["rights"] = "Youtube proprietary"

    return result







def vimeodata(vid):
    result = {}
    url = "http://vimeo.com/api/v2/video/{}.json".format(vid)
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    data = urllib2.urlopen(req).read()
    data = json.loads(data)[0]

    description = data["description"].replace("<br />", "").replace("\r", "").strip().replace("\n\n\n","\n\n")
    title = data["title"].strip()
    result["subject"] = data["tags"].strip()
    result["description"] = result["description/original"] = description
    result["title"] = result["title/original"] = title


    url = "http://vimeo.com/{}".format(vid)
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    data = urllib2.urlopen(req).read()

    if data.find("http://creativecommons.org/publicdomain/zero/1.0/") > -1:
        result["rights"] = "CC 0"
    elif data.find("http://creativecommons.org/licenses/by/3.0") > -1:
        result["rights"] = "CC BY 3.0"
    elif data.find("http://creativecommons.org/licenses/by-nc/3.0") > -1:
        result["rights"] = "CC BY-NC 3.0"
    elif data.find("http://creativecommons.org/licenses/by-nc-nd/3.0") > -1:
        result["rights"] = "CC BY-NC-ND 3.0"
    elif data.find("http://creativecommons.org/licenses/by-nc-sa/3.0") > -1:
        result["rights"] = "CC BY-NC-SA 3.0"
    elif data.find("http://creativecommons.org/licenses/by-nd/3.0") > -1:
        result["rights"] = "CC BY-ND 3.0"
    elif data.find("http://creativecommons.org/licenses/by-sa/3.0") > -1:
        result["rights"] = "CC BY-SA 3.0"
    else:
        result["rights"] = "Vimeo proprietary"

    return result





class Plugin(WorkerPlugin):
    def on_init(self):
        logging.goodnews("{} ({}) initialized".format(__manifest__["name"], __manifest__["description"]))

    def on_main(self):
        db = DB()
        for source, ident, parser in [
                ["Youtube" , "identifier/youtube", youtubedata],
                ["Vimeo" , "identifier/vimeo", vimeodata]
                ]:

            db.query("SELECT a.id_object FROM nx_meta as m, nx_assets as a WHERE m.object_type=0 and m.id_object = a.id_object AND a.id_folder = 10 AND a.origin='Production' AND  tag='source' and value=%s", [source])
            for id_asset, in db.fetchall():
                asset = Asset(id_asset, db=db)

                if asset["qc/state"] == 3:
                    continue

                if asset["title"] != asset[ident]:
                    continue

                logging.debug("Updating metadata {}".format(asset))

                try:
                    data = parser(asset[ident])
                except:
                    logging.warning("Failed to fetch metadata for asset {}".format(asset))
                    asset["title"] = asset["title"] + " (failed to load metadata)"
                    asset.save()
                    continue

                for key in data:
                    asset[key] = data[key]
                logging.info("Updated {}".format(asset))
                asset.save()

