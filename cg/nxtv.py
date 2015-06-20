# -*- coding: utf-8 -*-

def ticker(self,text):
    try: text = unicode(text,"utf-8")
    except: pass
    text = text.upper()
    self.set_color("text_background")
    self.rect(0,self.SAFET,1920,48)
    self.set_font("ticker")
    self.set_color("text_white")
    self.ctx.move_to(self.SAFEL,self.SAFET + 38)
    self.ctx.show_text(text)
    self.ctx.stroke()

def clock(self,tstamp):
    self.rect(1700,self.SAFET,1920,48,"#000000ff")
    self.set_font("ticker")
    self.set_color("text_white")
    self.ctx.move_to(1720,self.SAFET + 38)
    self.ctx.show_text(tstamp)
    self.ctx.stroke()

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

def music_label2(self,title,artist):
    """
    Song title and artist in ticker area (used when PIP is enabled)
    """
    self.set_font('ticker')
    tx, ty, artist_w, th, dx, dy = self.ctx.text_extents(artist) 
    tx, ty, title_w, th, dx, dy  = self.ctx.text_extents(title) 
    self.set_color("text_background")
    self.rect(0,self.SAFET+78, self.SAFEL + artist_w + title_w + 40 ,48)
    self.set_color("text_body")
    self.ctx.move_to(self.SAFEL,self.SAFET + 78 + 38)
    self.ctx.show_text(artist) 
    self.ctx.stroke()
    self.set_color("text_head")
    self.ctx.move_to(self.SAFEL + artist_w + 20 ,self.SAFET + 78 + 38)
    self.ctx.show_text(title)
    self.ctx.stroke()


def subtitle(self,titles):
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


def text_area(self, text, header=False):
    size=84
    header_size=96
    x, y,  = self.SAFEL, 350
    pad_lft = 25
    pad_rgt = 25
    pad_top = 20
    pad_btm = 20
    spacing = 20
    header_top = 216
    
    self.ctx.select_font_face('Bebas Neue', cairo.FONT_SLANT_NORMAL)

    if header:
        self.ctx.set_font_size(header_size)
        tw,th = self.ctx.text_extents(header)[2:4]
        if tw < 1200:
            self.set_color("text_background")
            self.rect(self.SAFEL-pad_lft, 216, tw+pad_lft+pad_rgt, th+pad_top+pad_btm)

            self.ctx.move_to(self.SAFEL,header_top+header_size)
            self.set_color("text_head")
            self.ctx.show_text(header)
            self.ctx.stroke()

    self.ctx.set_font_size(size)
     
    lines = []
    line = ""
    rem = ""
    tw = 1200
    max_w = 0
    for word in text.split(" "):
        if len(word) == 1 or (len(word) < 5 and word.endswith(".")): #and word not in string.digits:
            rem = word
            continue
        buff = " ".join([line,rem,word])
        if rem: word = " ".join([rem,word])
        lw = self.ctx.text_extents(buff)[2]
        if lw > tw:
            lines.append(line)
            line = word
        else:
            max_w = max(max_w, lw)
            line = ("%s %s" % (line,word)).strip()
        rem = ""
    lines.append(line)

    y+= spacing
    
    self.set_color("text_background")
    self.rect(self.SAFEL-pad_lft, y, max_w + pad_lft + pad_rgt, (th+spacing)*len(lines)+pad_top+pad_btm)

    self.set_color("text_body")
    y+= size
    for i,line in enumerate(lines): 
        tw,th = self.ctx.text_extents(line)[2:4]
        self.ctx.move_to(x,y+pad_top+(i*(size+spacing)))
        self.ctx.show_text(line)
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

