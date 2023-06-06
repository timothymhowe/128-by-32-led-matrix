from PIL import Image
# function for joining images horizontally
def concat_images_horizontally(image_1,image_2):
    new_im = Image.new("RGB",(image_1.width + image_2.width,max(image_1.height,image_2.height)))
    new_im.paste(image_1,(0,0))
    new_im.paste(image_2,(image_1.width,0))
    return new_im

# function for joining images vertically
def concat_images_vertically(image_1,image_2):
    new_im = Image.new("RGB",(max(image_1.width,image_2.width),image_1.height+image_2.height))
    new_im.paste(image_1,(0,0))
    new_im.paste(image_2,(0,image_1.height))
    return new_im
