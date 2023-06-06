from PIL import Image, ImageDraw, ImageFont, ImageOps
from concat_images import concat_images_horizontally, concat_images_vertically

# declaring constant for the font for the panel
THE_FONT = ImageFont.truetype('./fonts/apple2.ttf',8)
# THE_FONT = ImageFont.truetype('./fonts/DePixelKlein.ttf',8)
THE_FONT_SM = ImageFont.truetype('./fonts/DePixelIllegible.ttf',8)

class TeamBug:
    def __init__(self, code,color=(255,255,255),logos=True):
        self.code = code
        self.text = code.upper()
        self.color = color
        self.score = 0
        self.logo = Image.open(f"./images/nba/{self.code}.png").convert("RGBA")
        self.logo_small = self.logo.copy()
        self.logo_small.thumbnail((11,11),Image.ANTIALIAS)
        self.logo_small = ImageOps.expand(self.logo_small,border=2,fill="black")
        self.score = "0"
        
        self.label = None
        self.score_tile = None
        
        self.bug = None

        
    
    def build_label(self):
        txt = Image.new("RGB", (28,12),(0,0,0))
        
        d = ImageDraw.Draw(txt)
        # draw the road  team text
        d.text((1, 4), self.text, font=THE_FONT, fill=self.color)
        self.label = concat_images_horizontally(self.logo_small,txt)
        # self.label = concat_images_horizontally(foo,spacer.resize((1,16)))
        
    def build_score_tile(self):
        txt = Image.new("RGB",(11,12),(0,0,0))
        d = ImageDraw.Draw(txt)
        d.text((3,4),self.score,font=THE_FONT,fill=(200,200,200))
        self.score_tile = txt
        
    def build_bug(self):
        if self.label == None:
            self.build_label()
            
        if self.score_tile == None:
            self.build_score_tile()

        self.bug = concat_images_horizontally(self.label,self.score_tile)
        
    # getter method for the bug
    def get_bug(self):
        if self.bug == None:
            self.build_bug()
        return self.bug

            
    
    def update_score(self,new_score:str):
        self.score = new_score
        self.build_score_tile()
        self.bug = concat_images_horizontally(self.label,self.score_tile)
        
class ClockBug:
    def __init__(self):
        self.time_remaining_min = 15
        self.time_remaining_sec = 0
        self.period = 1
        self.clock_tile = None
        self.period_tile = None
        self.clock_bug = None
        
    def build_clock_bug(self):
        txt = Image.new("RGB",(25,8),(0,0,0))
        d = ImageDraw.Draw(txt)
        d.text((4,4),f"{self.time_remaining_min}:{self.time_remaining_sec:02d}",font=THE_FONT_SM,fill=(200,200,200))
        self.clock_tile = txt
        
        txt2 = Image.new("RGB",(18,8),(0,0,0))
        d = ImageDraw.Draw(txt2)
        d.text((4,4),f"|   Q{self.period}",font=THE_FONT_SM,fill=(200,200,200))
        self.period_tile = txt2
        
        self.clock_bug = concat_images_horizontally(self.clock_tile,self.period_tile)
        
    def get_bug(self):
        if self.clock_bug == None:
            self.build_clock_bug()
            
        return self.clock_bug
        
    
    def update_period(self, new_period):
        pass
    
    def update_time_remaining(self,new_time):
        pass

