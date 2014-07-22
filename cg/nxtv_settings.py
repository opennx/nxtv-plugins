# -*- coding: utf-8 -*-

SAFET = 54 
SAFEL = 192
SAFER = 1920 - SAFEL
SAFEB = 1080 - SAFET

def fuzzy(self, f=.9,t=3):
    import random
    return random.uniform(f,t)

def set_color(self,clr):
    if   clr == "text_background": self.ctx.set_source_rgba(0,0,0,0.9)
    elif clr == "text_white":      self.ctx.set_source_rgb(0.9,0.9,0.9)
    elif clr == "text_head":       self.ctx.set_source_rgb(1,.53,.21)
    elif clr == "text_body":       self.ctx.set_source_rgb(.69,.78,.91)

def set_font(self, f, size=False):
    if   f == "ticker":            
        self.ctx.select_font_face('TeXGyreHeros', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        self.ctx.set_font_size(size or 36)

    elif   f == "default":            
        self.ctx.select_font_face('TeXGyreHeros', cairo.FONT_SLANT_NORMAL)
        self.ctx.set_font_size(size or 54)
