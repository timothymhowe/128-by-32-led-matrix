import time,sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

# import json and re for api calls
import json
import requests as re


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

#  hard coding these for now for testing purposes
logo_home = Image.open("./images/nhl/vgk.png")
logo_away = Image.open("./images/nhl/fla.png")

logo_home.thumbnail((matrix.width,matrix.height),Image.ANTIALIAS)
matrix.SetImage(logo_home.convert("RGB"))



# matrix.

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("stopping...")