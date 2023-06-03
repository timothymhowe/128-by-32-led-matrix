import time,sys,os

from time import strftime
from PIL import Image, ImageEnhance
from rgbmatrix import RGBMatrixOptions, RGBMatrix, graphics

class ClockNumber:
    def __init__():
        print("Sup Fam bruh")







options = RGBMatrixOptions()

options.rows = 32
options.cols = 64
options.chain_length = 2
options.gpio_slowdown = 4
options.led_rgb_sequence = "RBG"

options.hardware_mapping ='adafruit-hat-pwm'

matrix=RGBMatrix(options=options)

# matrix.SetImage(image_h0.convert("RGB"))


the_canvas = matrix.CreateFrameCanvas()
pos = the_canvas.width


tube_dict = {   
                '0':Image.open("./images/nixie/0.png").convert("RGB"),
                '1':Image.open("./images/nixie/1.png").convert("RGB"),
                '2':Image.open("./images/nixie/2.png").convert("RGB"),
                '3':Image.open("./images/nixie/3.png").convert("RGB"),
                '4':Image.open("./images/nixie/4.png").convert("RGB"),
                '5':Image.open("./images/nixie/5.png").convert("RGB"),
                '6':Image.open("./images/nixie/6.png").convert("RGB"),
                '7':Image.open("./images/nixie/7.png").convert("RGB"),
                '8':Image.open("./images/nixie/8.png").convert("RGB"),
                '9':Image.open("./images/nixie/9.png").convert("RGB")
            }

img_spacer = Image.open("./images/nixie/spacer_2w.png").convert("RGB")

def concat_images_horizontally(image_1,image_2):
    new_im = Image.new("RGB",(image_1.width + image_2.width,image_1.height))
    new_im.paste(image_1,(0,0))
    new_im.paste(image_2,(image_1.width,0))
    return new_im

# method for creating a pair of nixie tube numerals for the clock
def create_tube_pair_image(int1,int2):
    temp = concat_images_horizontally(tube_dict[int1],img_spacer)
    return concat_images_horizontally(temp,tube_dict[int2])


# get current system time from the rtc as a string
def get_timestamp_from_rtc():
    current_time_str = time.strftime("%H%M%S",time.localtime())
    return current_time_str

curr_time = get_timestamp_from_rtc()
#  create all the number pair images
hh = create_tube_pair_image(curr_time[0],curr_time[1])
mm = create_tube_pair_image(curr_time[2],curr_time[3])
ss = create_tube_pair_image(curr_time[4],curr_time[5])

# print(time.clock_gettime())
matrix.SetImage(hh.convert("RGB"))

def create_spacer():
    foo = concat_images_horizontally(img_spacer,img_spacer)
    foo = concat_images_horizontally(foo,img_spacer)
    foo = concat_images_horizontally(foo,img_spacer)
    return foo

big_spacer = create_spacer()

def create_full_clock_image(H,M,S):
    foo = concat_images_horizontally(H,big_spacer)
    foo = concat_images_horizontally(foo,M)
    foo = concat_images_horizontally(foo,big_spacer)
    foo = concat_images_horizontally(foo,S)
    foo = concat_images_horizontally(img_spacer,foo)
    foo = concat_images_horizontally(img_spacer,foo)
    foo = concat_images_horizontally(foo,img_spacer)
    foo = concat_images_horizontally(foo,img_spacer)
    foo = concat_images_horizontally(foo,img_spacer)
    return foo



font = graphics.Font()
# font.LoadFont("./fonts/courB18.bdf")
# font.LoadFont("../../rpi-rgb-led-matrix/fonts/9x18.bdf")


try:
    print("Press CTRL-C to stop display.")
    while True:
        last_time = curr_time
        curr_time = get_timestamp_from_rtc()
        if (last_time != curr_time):
            ss=create_tube_pair_image(curr_time[4],curr_time[5])
            if curr_time[3] != last_time[3]:
                mm = create_tube_pair_image(curr_time[2],curr_time[3])
                if curr_time[1] != last_time[1]:
                    hh = create_tube_pair_image(curr_time[0],curr_time[1])

        bar = create_full_clock_image(hh,mm,ss)
        enhancer = ImageEnhance.Color(bar)
        bar = enhancer.enhance(1.5)
        matrix.SetImage(bar.convert("RGB"))

        # the_canvas.Clear()
        # matrix.SetImage(image.convert("RGB"))
        # pos -= 1
        # if (pos + len < 0):
        #     pos = the_canvas.width
        time.sleep(0.5)

        # the_canvas = matrix.SwapOnVSync(the_canvas)

except KeyboardInterrupt:
    print("\n Stopping dislpay.")
    sys.exit(0)