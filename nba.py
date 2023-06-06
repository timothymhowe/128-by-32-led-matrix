import time,sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageDraw, ImageFont, ImageOps
from scorebug import TeamBug, ClockBug

# import json and re for api calls
import json
import requests as re

# declaring constant for the font for the panel
THE_FONT = ImageFont.truetype('./fonts/8-bit-hud.ttf',6)
# THE_FONT = ImageFont.truetype('./fonts/DePixelKlein.ttf',8)
THE_FONT_SM = ImageFont.truetype('./fonts/DePixelIllegible.ttf',8)

# options for the RGB matrix controlled by the adafruit hat with RTC and PWM.  TODO: need to create a generic object for this 
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 2
options.gpio_slowdown = 4
options.led_rgb_sequence = "RBG"
options.hardware_mapping ='adafruit-hat-pwm'
matrix=RGBMatrix(options=options)

the_canvas = matrix.CreateFrameCanvas()

# function for creating images horizontally
def concat_images_horizontally(image_1,image_2):
    new_im = Image.new("RGB",(image_1.width + image_2.width,max(image_1.height,image_2.height)))
    new_im.paste(image_1,(0,0))
    new_im.paste(image_2,(image_1.width,0))
    return new_im

def concat_images_vertically(image_1,image_2):
    new_im = Image.new("RGB",(max(image_1.width,image_2.width),image_1.height+image_2.height))
    new_im.paste(image_1,(0,0))
    new_im.paste(image_2,(0,image_1.height))
    return new_im




#  hard coding these for now for testing purposes
road_code = "mia"
home_code = "den"

# with Image.open(f"./images/nhl/{road_code}.png").convert("RGBA") as logo_road:
#     txt = Image.new("RGB", (28,16),(0,0,0))
#     fnt = ImageFont.truetype('./fonts/pkmn.ttf',8)
#     d = ImageDraw.Draw(txt)
#     # draw the r0ad  team text
#     d.text((2, 4), road_code.upper(), font=fnt, fill=(4, 30, 66, 255))
    
#     logo_road.thumbnail((12,100),Image.ANTIALIAS)
#     logo_road = ImageOps.expand(logo_road,border=2,fill="black")

#     road_bug = concat_images_horizontally(logo_road,txt)

        
    

# with Image.open(f"./images/nhl/{home_code}.png").convert("RGBA") as logo_home:
#     # if logo_home.mode != "RGBA":
#         # logo_home.convert("RGBA").save("vgk2.png",'PNG')
#     txt = Image.new("RGB", (28,16),(0,0,0))
#     # load the font
   
#     # initialize the drawing instance
#     d = ImageDraw.Draw(txt)
    
#     # draw the home team text
#     d.text((2, 4), home_code.upper(), font=THE_FONT, fill=(180, 151, 90, 255))
  
    
#     logo_home.thumbnail((12,100),Image.ANTIALIAS)
#     logo_home = ImageOps.expand(logo_home,border=2,fill="black")

#     home_bug = concat_images_horizontally(logo_home,txt)

spacer = Image.open("./images/nixie/spacer_2w.png")

# class to handle the scorebug, and updating the scores 
class NBATeamBug(TeamBug):
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
        txt = Image.new("RGB", (28,16),(0,0,0))
        
        d = ImageDraw.Draw(txt)
        # draw the road  team text
        d.text((2, 4), self.text, font=THE_FONT, fill=self.color)
        self.label = concat_images_horizontally(self.logo_small,txt)
        # self.label = concat_images_horizontally(foo,spacer.resize((1,16)))
        
    def build_score_tile(self):
        txt = Image.new("RGB",(11,16),(0,0,0))
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
        
class NBAClockBug(ClockBug):
    def __init__(self):
        self.time_remaining_min = 15
        self.time_remaining_sec = 0
        self.max_periods = 4
        self.period = 1
        self.clock_tile = None
        self.period_tile = None
        self.clock_bug = None
        
    def build_clock_bug(self):
        txt = Image.new("RGB",(42,16),(0,0,0))
        d = ImageDraw.Draw(txt)
        d.text((4,4),f"{self.time_remaining_min}:{self.time_remaining_sec:02d}",font=THE_FONT_SM,fill=(200,200,200))
        self.clock_tile = txt
        
        txt2 = Image.new("RGB",(18,16),(0,0,0))
        d = ImageDraw.Draw(txt2)
        d.text((4,4),f"P{self.period}",font=THE_FONT_SM,fill=(200,200,200))
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

    
road = TeamBug("mia",(152, 0, 46))
home = TeamBug("den",(13, 34, 64))
clock = ClockBug()

full_bug = concat_images_vertically(road.get_bug(),clock.get_bug())
full_bug = concat_images_vertically(full_bug,home.get_bug())
full_bug = concat_images_horizontally(full_bug,spacer.resize((1,32)))

court = Image.open('./images/nba/court.png')
pasted = Image.new("RGBA",(75,32),"BLACK")
pasted.paste(court,(9,0),court)
full_bug = concat_images_horizontally(full_bug,pasted)
matrix.SetImage(full_bug.convert("RGB"))


def get_live_data(game_id,timecode=time.gmtime()):
   pass


try:
    while True:
        time.sleep(5)
        
except KeyboardInterrupt:
    print("Shutting down...")