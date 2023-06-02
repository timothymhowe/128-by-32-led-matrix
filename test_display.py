# importing required dependencies, PIL
from PIL import Image   
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

import time, sys


if len(sys.argv)<2:
    sys.exit("Please provide an image argument.")
else:
    image_file = sys.argv[1]

image = Image.open(image_file)

options = RGBMatrixOptions()

options.rows = 32
options.cols = 64
options.chain_length = 2
options.gpio_slowdown = 3

options.hardware_mapping ='adafruit-hat'

matrix=RGBMatrix(options=options)

image.thumbnail((matrix.width,matrix.height),Image.ANTIALIAS)

matrix.SetImage(image.convert("RGB"))
print(matrix.width)
print(matrix.height)

offscreen_canvas = matrix.CreateFrameCanvas()
pos = offscreen_canvas.width
text_color = graphics.Color(255,255,0)
font = graphics.Font()
font.LoadFont("./fonts/courB18.bdf")
# font.LoadFont("./fonts/pkmn.fnt")


 
try:
    print ("Press CTRL-C to stop display.")
    while True:
        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas,font,pos,22,text_color,"Hello World")
        pos -= 1
        if (pos + len < 0):
            pos = offscreen_canvas.width
        
        time.sleep(0.05)

        offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)


except KeyboardInterrupt:
    print("\nClosing...")
    sys.exit(0)