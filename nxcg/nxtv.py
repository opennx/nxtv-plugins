# -*- coding: utf-8 -*-
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
                "text_area_head_font" : "TeXGyreHeros Bold 48",
                "text_area_body_font" : "Raleway 40",
                "text_area_body_color" : "#b0c7e8",
            }


    def ticker(self, *args, **kwargs):
        return self.cg.nxkit_ticker(*args, **kwargs)

    def clock(self, *args, **kwargs):
        return self.cg.nxkit_clock(*args, **kwargs)

    def text_area(self, *args, **kwargs):
        return self.cg.nxkit_text_area(*args, **kwargs)

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

    def vedci_zjistili(self):
        import random
        try:
            data = open("/mnt/nxtv_02/Library/vedci_zjistili.txt").read()
            text = random.choice([i.strip() for i in data.strip().split("\n")])
        except:
            text = """že soubor s tím, co zjistili, není k dispozici"""
        self.text_area("Vědci zjistili", text)

    def vedeli_jste(self):
        import random
        try:
            data = open("/mnt/nxtv_02/Library/vedeli_jste.txt").read()
            text = random.choice([i.strip() for i in data.strip().split("\n")])
        except:
            text = """tahle grafika nám zrovna nefunguje"""
        self.text_area("Věděli jste?", text)


    def program(self, header, items):
        size=84
        header_size=96
        x, y,  = self.SAFEL, 370
        pad_lft = 25
        pad_rgt = 25
        pad_top = 20
        pad_btm = 20
        spacing = 150
        header_top = 216

        self.ctx.select_font_face('Bebas Neue', cairo.FONT_SLANT_NORMAL)
        if header:
            self.ctx.set_font_size(header_size)
            tw,th = self.ctx.text_extents(header)[2:4]

            self.set_color("text_background")
            self.rect(self.SAFEL-pad_lft, 216, tw+pad_lft+pad_rgt, th+pad_top+pad_btm)

            self.ctx.move_to(self.SAFEL,header_top+header_size)
            self.set_color("text_head")
            self.ctx.show_text(header)
            self.ctx.stroke()

        self.ctx.set_font_size(size)
        i=-1
        for ts, title in items:
            i+=1
            tw,th = self.ctx.text_extents(title)[2:4]

            self.set_color("text_background")
            self.rect(self.SAFEL-pad_lft, y, 210, 105)
            self.rect(self.SAFEL + 250, y, tw + pad_lft+ pad_rgt, 105)

            self.set_color("text_body")
            self.ctx.move_to(self.SAFEL,y+size)
            self.ctx.show_text(ts)
            self.ctx.stroke()

            self.ctx.move_to(self.SAFEL + 250 + pad_lft, y+size)
            self.ctx.show_text(title)
            self.ctx.stroke()


            y+= spacing


