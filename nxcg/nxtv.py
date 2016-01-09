from nxcg.plugin import NXCGPlugin
from nxcg.utils import textify


class Plugin(NXCGPlugin):
    def on_init(self):
        self.cg.nx_kit = {
                "ticker_position" : "top",
                "text_color"      : "#b0c7e8",
            }


    def music_label(self,title,artist):
        self.set_font("default", 72)
        tx, ty, title_w, th, dx, dy = self.ctx.text_extents(title)

        self.set_font("default", 54)
        tx, ty, artist_w, th, dx, dy = self.ctx.text_extents(artist)
        mwidth = max(title_w,artist_w) + self.SAFEL + 40

        self.set_color("text_background")
        self.ctx.move_to(self.SAFEL - 30,   self.SAFEB - 65)
        self.ctx.line_to(mwidth,            self.SAFEB - 90)
        self.ctx.line_to(mwidth+35,         self.SAFEB - 255)
        self.ctx.line_to(self.SAFEL -40,    self.SAFEB - 280)
        self.ctx.fill()

        self.set_font("default", 72)
        self.ctx.move_to(self.SAFEL,self.SAFEB-175)
        self.set_color("text_head")
        self.ctx.show_text(title)
        self.ctx.stroke()

        self.set_font("default", 54)
        self.ctx.move_to(self.SAFEL,self.SAFEB-105)
        self.set_color("text_body")
        self.ctx.show_text(artist)
        self.ctx.stroke()



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


