# -*- coding: utf-8 -*-

from nx import *
from nx.cg import CG
from nx.plugins import PlayoutPlugin

__manifest__ = {
    "name"        : "Subtitles",
    "description" : "Simple SRT subtitles burn-in",
    "author"      : "martas@imm.cz"
}

class Plugin(PlayoutPlugin):
    def on_init(self):
        self.id_layer    = 11
        self.subs_offset = -10
        self.image_file  = os.path.join(storages[3].get_path(), "media.dir", "cg_subtitle.png")


    def on_change(self):
        self.subs = []

        if self.load_subs():
            self.next_start = 0
            self.next_stop = 0
            self.tasks = [self.make_sub, self.show_sub]
        else:
            self.tasks = []
            self.query("CLEAR {}".format(self.layer()))


    def load_subs(self):
        srt_file  = os.path.splitext(self.channel.current_asset.get_file_path())[0] + ".srt"
        
        if os.path.exists(srt_file):
            for block in open(srt_file,"rU").read().split("\n\n"):
                try:
                    block  = block.split("\n")
                    tcodes = block[1]
                    lines  = block[2:]
                except:
                    continue
                start, stop = tcodes.split("-->")
                start = self.parse_tc(start)
                stop  = self.parse_tc(stop) 
                self.subs.append((start,stop,lines))
            return True
        else:
            return False
   

    def parse_tc(self, tcode, tbase=25):
        hh,mm,ss = tcode.strip().split(":")
        hh = int(hh)
        mm = int(mm)
        ss = float(ss.replace(",","."))
        return (hh*3600*tbase) + (mm*60*tbase) + (ss*tbase)
    
        
    def make_sub(self):
        try:    
            self.next_start, self.next_stop, titles = self.subs.pop(0)
        except: 
            self.next_start = self.next_stop = False
            return False  
        
        c = CG()
        c.subtitle(titles)
        c.save(self.image_file)
        return True
     
     
    def show_sub(self):
        if self.channel.fpos > self.next_start + self.subs_offset:
            self.query("PLAY %s cg_subtitle" % self.layer())
            self.current_stop = self.next_stop
            self.make_sub() 
            self.tasks.append(self.hide_sub)
            return True
        else:
            return False
      
      
    def hide_sub(self):
        if self.channel.fpos > self.current_stop + self.subs_offset:
            self.query("CLEAR %s" % self.layer())
            if self.next_start:
                self.tasks.append(self.show_sub)
            return True
 