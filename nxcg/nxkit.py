from nxcg.plugin import NXCGPlugin
from nxcg.utils import textify

class Plugin(NXCGPlugin):
    def on_init(self):
        self.cg.nx_kit_defaults = {
                "ticker_position" : "bottom",
                "ticker_height" : 48,
                "ticker_voffset" : 2,
                "ticker_font" : "Roboto Medium 26",
                "ticker_background" : "black glass 75",
                "ticker_color" : "white",
                "clock_position" : "right",
                "clock_width" : 100,
                "clock_font" : "Roboto Bold 26",
                "clock_background" : "black",
                "clock_color" : "white",
            }


    def __param(self, key):
        if hasattr(self.cg, "nx_kit") and key in self.cg.nx_kit:
            return self.cg.nx_kit
        return self.cg.nx_kit_defaults


    def __ticker_y(self):
        if self.__param("ticker_position") == "bottom":
            return self.cg.height - self.cg.safe.b - self.__param("ticker_height")
        else:
            return self.cg.safe.t


    def nx_kit_ticker(self, text):
        text = textify(text)
        self.cg.set_color(self.__param("ticker_background"))
        self.cg.rect(0, self.__ticker_y, self.cg.width, self.__param("ticker_height"))
        self.cg.text(text,
                pos=(self.cg.safe.l, self.__ticker_y + self.__param("ticker_voffset")),
                color=self.__param("ticker_color"),
                font=self.__param("ticker_font"),
            )


#TODO
    def nx_kit_clock(self, tstamp):
        self.cg.set_color(self._param("clock_background"))
        self.cg.rect(self.clock_x, self.__ticker_y, self.cg.width - self.clock_x, self.ticker_h)
        a,b = self.cg.text(tstamp,
                pos=(self.clock_x + 14, self.ticker_y + self.ticker_voffset),
                color="text_tick",
                font=FONT_CLOCK
            )


#TODO
    def nx_kit_crawl(self, text):
        text = textify(text)
        w, h = self.cg.text(text,
            font=FONT_CRAWL,
            color="text_crawl",
            spacing=0,
            render=False
            )
        top = SAFET + 48
        self.cg.new(w, 1080)
        self.cg.set_color("black glass 75")
        self.cg.rect(0, top, w, 54)
        self.cg.text(text ,
            pos=(0, top+1),
            font=FONT_CRAWL,
            color="text_crawl",
            spacing=0
            )


#TODO
    def nx_kit_text_area(self, header, text, source=False):
        header = textify(header).upper()
        text = textify(text)
        off = 160
        wi = 1200
        pad_h = 20
        ### Header
        x = self.cg.safe.l
        y = self.cg.safe.t + off
        w, h = self.cg.text(header,
            font=FONT_HEAD,
            color="gold",
            width=wi,
            spacing=0,
            render=False
            )
        self.cg.set_color("sport grey 80")
        self.cg.rect(x-pad_h, y-5, w+(pad_h*2), h+10)
        self.cg.text_render(x, y)
        ### Text
        y = self.cg.safe("t") + off + h + 40
        w, h = self.cg.text(text ,
            font=FONT_BODY,
            color="text_tick",
            width=wi,
            spacing=0,
            render=False
            )
        self.cg.set_color("sport grey 80")
        self.cg.rect(x-pad_h, y-10, w+(pad_h*2), h+100)
        self.cg.text_render(x, y)


#TODO
    def nx_kit_subtitle(self,titles):
        self.ctx.select_font_face('TeXGyreHeros', cairo.FONT_SLANT_NORMAL,cairo.FONT_WEIGHT_BOLD)
        self.ctx.set_font_size(46)
        for i,text in enumerate(titles[::-1]):
            tx, ty, tw, th, dx, dy = self.ctx.text_extents(text)
            self.ctx.move_to((self.w/2)-(tw/2),self.SAFEB-(i*52))
            self.ctx.set_source_rgb (.1, .1, .1)
            self.ctx.set_line_width (4)
            self.ctx.text_path (text)
            self.ctx.stroke()
            self.ctx.move_to((self.w/2)-(tw/2),self.SAFEB-(i*52))
            self.ctx.set_line_width (0)
            self.ctx.set_source_rgb (.9, .9, .9)
            self.ctx.show_text(text)
            self.ctx.stroke()
