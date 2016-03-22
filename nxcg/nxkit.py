from nxcg.plugin import NXCGPlugin
from nxcg.utils import textify


class Plugin(NXCGPlugin):
    def on_init(self):
        self.cg.nxkit_defaults = {
                "ticker_position" : "bottom",
                "ticker_height" : 48,
                "ticker_voffset" : 2,
                "ticker_caps" : True,
                "ticker_font" : "Roboto Medium 26",
                "ticker_background" : "black glass 75",
                "ticker_color" : "white",
                "clock_position" : "right",
                "clock_width" : 100,
                "clock_font" : False,                                   # Inherit from ticker font
                "clock_color" : False,                                  # Inherit from ticker font
                "clock_background" : "black",
                "crawl_font" : False,
                "crawl_color" : False,
                "crawl_background" : False,
                "text_area_head_color" : "gold",
                "text_area_body_color" :  "white",
                "text_area_head_background" : "black glass 80",
                "text_area_body_background" : False,                    # Inherit form text area head
                "text_area_head_font" : "Roboto Medium 40",
                "text_area_body_font" : "Roboto Medium 36",
                "text_area_head_caps" : False,
                "text_area_body_caps" : False,
                "schedule_head_font" : False,
                "schedule_time_font" : False,
                "schedule_body_font" : False,
                "schedule_head_color" : False,
                "schedule_time_color" : False,
                "schedule_body_color" : False,
                "schedule_head_background" : False,
                "schedule_time_background" : False,
                "schedule_body_background" : False,
            }


    def nxkit_param(self, key):
        if hasattr(self.cg, "nxkit") and key in self.cg.nxkit:
            return self.cg.nxkit[key]
        return self.cg.nxkit_defaults[key]

    @property
    def nxkit_ticker_y(self):
        if self.nxkit_param("ticker_position") == "bottom":
            return self.cg.safe.b - self.nxkit_param("ticker_height")
        else:
            return self.cg.safe.t


    def nxkit_ticker(self, text):
        text = textify(text)
        if self.nxkit_param("ticker_caps"):
            text = text.upper()
        self.cg.set_color(self.nxkit_param("ticker_background"))
        self.cg.rect(0, self.nxkit_ticker_y, self.cg.width, self.nxkit_param("ticker_height"))
        self.cg.text(
                text,
                pos=(self.cg.safe.l, self.nxkit_ticker_y + self.nxkit_param("ticker_voffset")),
                color=self.nxkit_param("ticker_color"),
                font=self.nxkit_param("ticker_font"),
            )


    def nxkit_clock(self, tstamp):
        #TODO: Clock on left
        x = self.cg.safe.r - self.nxkit_param("clock_width")
        w = self.cg.width - x
        self.cg.set_color(self.nxkit_param("clock_background"))
        self.cg.rect(x, self.nxkit_ticker_y, w, self.nxkit_param("ticker_height"))
        a,b = self.cg.text(
                tstamp,
                pos=(x + 14, self.nxkit_ticker_y + self.nxkit_param("ticker_voffset")),
                color=self.nxkit_param("clock_color") or self.nxkit_param("ticker_color"),
                font=self.nxkit_param("clock_font") or self.nxkit_param("ticker_font")
            )


    def nxkit_crawl(self, text):
        #TODO: Position, safe areas...
        text = textify(text)
        w, h = self.cg.text(
            text,
            font=self.nxkit_param("crawl_font") or self.nxkit_param("ticker_font"),
            render=False
            )
        top = SAFET + 48
        self.cg.new(w, 1080)
        self.cg.set_color(self.nxkit_param("crawl_background") or self.nxkit_param("ticker_background"))
        self.cg.rect(0, top, w, 54)
        self.cg.text(
            text,
            pos=(0, top+1),
            font=self.nxkit_param("crawl_font") or self.nxkit_param("ticker_font"),
            color=self.nxkit_param("crawl_color") or self.nxkit_param("ticker_font"),
            spacing=0
            )


    def nxkit_text_area(self, header, text, source=False):
        header = textify(header).upper()
        text = textify(text)
        off = 160
        wi = 1200
        pad_h = 20
        ### Header
        x = self.cg.safe.l
        y = self.cg.safe.t + off
        w, h = self.cg.text(header,
            font=self.nxkit_param("text_area_head_font"),
            color=self.nxkit_param("text_area_head_color"),
            width=wi,
            spacing=0,
            render=False
            )
        self.cg.set_color(self.nxkit_param("text_area_head_background"))
        self.cg.rect(x-pad_h, y-5, w+(pad_h*2), h+10)
        self.cg.text_render(x, y)
        ### Text
        y = self.cg.safe("t") + off + h + 40
        w, h = self.cg.text(
            text,
            font=self.nxkit_param("text_area_body_font") or self.nxkit_param("text_area_head_font"),
            color=self.nxkit_param("text_area_body_color") or self.nxkit_param("text_area_head_color"),
            width=wi,
            spacing=0,
            render=False
            )
        self.cg.set_color(self.nxkit_param("text_area_body_background") or self.nxkit_param("text_area_head_background"))
        self.cg.rect(x-pad_h, y-10, w+(pad_h*2), h+80)
        self.cg.text_render(x, y)


    def nxkit_schedule(self, header, schedule):
        off = 160
        wi = 1200
        pad_h = 20
        pad_v = 5
        ### Header
        x = self.cg.safe.l
        y = self.cg.safe.t + off
        w, h = self.cg.text(header,
            font=self.nxkit_param("schedule_head_font") or self.nxkit_param("text_area_head_font"),
            color=self.nxkit_param("schedule_head_color") or self.nxkit_param("text_area_head_color"),
            width=wi,
            spacing=0,
            render=False
            )
        self.cg.set_color(self.nxkit_param("schedule_head_background") or self.nxkit_param("text_area_head_background"))
        self.cg.rect(x-pad_h, y-5, w+(pad_h*2), h+10)
        self.cg.text_render(x, y)

        tw, th = self.cg.text(
                "22:55",
                font=self.nxkit_param("schedule_time_font") or self.nxkit_param("text_area_body_font"),
                width=wi,
                spacing=0,
                render=False
                )

        tw += pad_h*2
        th += pad_v*2
        lx = x + 220

        for i, line in enumerate(schedule):
            # Timestamp
            y += h + 40
            w, h = self.cg.text(
                line[0],
                font=self.nxkit_param("schedule_time_font") or self.nxkit_param("text_area_body_font"),
                color=self.nxkit_param("schedule_time_color") or self.nxkit_param("text_area_body_color"),
                width=wi,
                spacing=0,
                render=False
                )
            self.cg.set_color(self.nxkit_param("text_area_body_background") or self.nxkit_param("text_area_head_background"))
            self.cg.rect(x-pad_h, y-pad_v, tw, th)
            self.cg.text_render(x, y)

            # Program name
            w, h = self.cg.text(
                line[1],
                font=self.nxkit_param("schedule_body_font") or self.nxkit_param("text_area_body_font"),
                color=self.nxkit_param("schedule_body_color") or self.nxkit_param("text_area_body_color"),
                width=wi,
                spacing=0,
                render=False
                )
            self.cg.set_color(self.nxkit_param("text_area_body_background") or self.nxkit_param("text_area_head_background"))
            self.cg.rect(lx-pad_h,  y-pad_v, w+(pad_h*2), h+(pad_v*2))
            self.cg.text_render(lx, y)


#TODO
    def nxkit_subtitle(self,titles):
        return
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

