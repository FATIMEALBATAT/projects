from PIL import Image

def resizePic(pic, size=(100,100)): # Center Pic 
    picwidth, picheight = pic.size
    ratio = picwidth / picheight

    new_height = size[1]
    new_width = int(ratio * new_height)
    newPic = pic.resize((new_width, new_height))
    picwidth, picheight = newPic.size
    newPic = newPic.crop(((picwidth-size[0])/2, (picheight-size[1])/2, (picwidth+size[0])/2, (picheight+size[1])/2))
    return newPic