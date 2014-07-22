# -*- coding: utf-8 -*-

def vedci_zjistili(self):
    try:    
        data = open("/mnt/nx02/Library/vedci_zjistili.txt").read()
        text = random.choice([i.strip() for i in data.strip().split("\n")])
    except: 
        text = """že soubor s tím, co zjistili, není k dispozici"""
    self.text_area(text, "Vědci zjistili")
 



def weather_small(self,dataset=False):
    if not dataset:
        ICON_DIR = "meteo_icons"
        dataset = [
            ("Praha", 7, 302),
            ("Plzeň", 12, 317),
            ("Č. Budějovice", 8, 362),
            ("Liberec", 3, 200)
            ]
    else:
        ICON_DIR = "/mnt/nx01/.nx/mod_weather/icons"
    
    self.set_color("text_background")
    self.rect(1562, 216, 261, 714)
    top = 264 
    left = 1578
    self.ctx.select_font_face('TeXGyreHerosCn', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    for title, temp_c, weather_code in dataset:
        icon_path    = os.path.join(ICON_DIR,"%s.png"%weather_code)
        icon = cairo.ImageSurface.create_from_png(icon_path)

        self.set_color("text_head")
        self.ctx.set_font_size(36)
        
        self.ctx.move_to(left , top)
        self.ctx.show_text(title)
        self.ctx.stroke()
 
        self.set_color("text_body")
        self.ctx.set_font_size(56)
        self.ctx.move_to(left + 120, top + 75)  
        self.ctx.show_text("{}\u00b0".format(temp_c))
        self.ctx.stroke()
        
        icnx = left
        icny = top + 18 
        icsz = 76

        self.ctx.set_source_surface(icon,icnx,icny)
        self.ctx.rectangle(icnx,icny,icnx+icsz,icny+icsz)
        self.ctx.fill()
 
        top += 170
