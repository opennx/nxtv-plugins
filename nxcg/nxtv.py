# -*- coding: utf-8 -*-

import random

from nxcg.plugin import NXCGPlugin
from nxcg.utils import textify


class Plugin(NXCGPlugin):
    def on_init(self):
        self.cg.safe_vals["th"] = .05 # no reason to have 10% safe area on internet
        self.cg.nxkit = {
                "ticker_position" : "top",
                "ticker_caps" : True,
                "ticker_font" : "TeXGyreHeros Bold 24",
                "ticker_color" : "#cccccc",
                "clock_font" : "TeXGyreHeros Bold 24",
                "clock_color" : "#cccccc",
                "ticker_voffset" : 2,
                "text_area_head_font" : "TeXGyreHeros Bold 40",
                "text_area_body_font" : "TeXGyreHeros 40",
                "text_area_body_color" : "#b0c7e8",
                "schedule_time_font" : "TeXGyreHeros Bold 36",
                "schedule_body_font" : "TeXGyreHeros 36",
            }

    def ticker(self, *args, **kwargs):
        return self.cg.nxkit_ticker(*args, **kwargs)

    def clock(self, *args, **kwargs):
        return self.cg.nxkit_clock(*args, **kwargs)

    def text_area(self, *args, **kwargs):
        return self.cg.nxkit_text_area(*args, **kwargs)

    def schedule(self, *args, **kwargs):
        return self.cg.nxkit_schedule(*args, **kwargs)

    def program(self, *args, **kwargs): # DEPRECATED ALIAS
        return self.cg.nxkit_schedule(*args, **kwargs)

    def subtitle(self, *args, **kwargs):
        return self.cg.nxkit_subtitle(*args, **kwargs)

    #
    # NXTV Specific widgets
    #

    def music_label(self,title,artist):
        font_title = "Raleway 54"
        font_artist = "Raleway 38"
        title=textify(title)
        artist=textify(artist)
        title_w, h = self.cg.text(
            title,
            font=font_title,
            render=False
            )
        artist_w, h = self.cg.text(
            artist,
            font=font_artist,
            render=False
            )
        mwidth = max(title_w, artist_w) + self.cg.safe.l + 40

        points = [
            [self.cg.safe.l - 30, self.cg.safe.b - 65],
            [mwidth, self.cg.safe.b - 90],
            [mwidth + 35, self.cg.safe.b - 255],
            [self.cg.safe.l - 40, self.cg.safe.b - 280]
            ]

        self.cg.set_color("black glass 75")
        self.cg.polygon(*points)

        title_w, h = self.cg.text(
            title,
            font=font_title,
            color="gold",
            pos=(self.cg.safe.l, self.cg.safe.b - 250)
            )
        artist_w, h = self.cg.text(
            artist,
            font=font_artist,
            color="#b0c7e8",
            pos=(self.cg.safe.l, self.cg.safe.b - 160)
            )

    #
    # Text areas (videotext)
    #

    def vedci_zjistili(self):
        try:
            data = open("/mnt/nxtv_01/Library/vedci_zjistili.txt").read()
            text = random.choice([i.strip() for i in data.strip().split("\n")])
        except:
            text = """že soubor s tím, co zjistili, není k dispozici"""
        self.text_area("Vědci zjistili", text)

    def vedeli_jste(self):
        try:
            data = open("/mnt/nxtv_01/Library/vedeli_jste.txt").read()
            text = random.choice([i.strip() for i in data.strip().split("\n")])
        except:
            text = """tahle grafika nám zrovna nefunguje"""
        self.text_area("Věděli jste?", text)
