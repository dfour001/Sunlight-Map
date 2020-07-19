from PIL import Image, ImageEnhance, ImageFilter
import os

##    Required paths:
##        inputPath - The path that will contain each of the input images
##        outputPath - The path where any output images will be saved
##        maskPath - The path to the greyscale mask image.
##            Black = Areas to analyze
##            White = Areas to ignore

inputPath = r'C:\Users\danie\Documents\Python\Sunlight-Map\test'
outputPath = r'C:\Users\danie\Documents\Python\Sunlight-Map\test\output'
maskPath = r'C:\Users\danie\Documents\Python\Sunlight-Map\mask.jpg'

def main():
    # imgs is a list containing the names of each of the jpg images located in the
    # inputPath.
    imgs = [file for file in os.listdir(inputPath) if '.' in file and file.split('.')[1].lower() == 'jpg']

    # Sunmaps show areas of direct sunlight.  These areas are added together to
    # determine how much each area is exposed to sunlight.  sunmaps is a list
    # consisting of pillow image objects.
    sunmaps = []

    for img in imgs:
        inputImg = Image.open(inputPath + '\\' + img)

        if maskPath:
            inputMask = Image.open(maskPath)
        else:
            inputMask = None

        sunMap = create_sunlight_map(inputImg, inputMask)
        outputFile = img.split('.')[0] + '_sunMap.jpg'
        sunMap.save(outputPath + '\\' + outputFile)
        create_sunlight_map_overlay(inputImg, sunMap, img)


def create_sunlight_map(img, mask, v=229, show=False, saveBW=False):
    # Convert to BW image
    print(img)
    imgBW = img.convert("L")

    if mask:
        mask = mask.convert("L")

    # Blur image
##    imgBW = imgBW.filter(ImageFilter.GaussianBlur(5))
    imgBW = imgBW.filter(ImageFilter.GaussianBlur(3))

    # Increase Contrast
    cont = ImageEnhance.Contrast(imgBW)
##    imgBW = cont.enhance(3)
    imgBW = cont.enhance(2.5)

    if saveBW:
        imgBW.save(outputPath + '\\' + img.filename.split('\\')[-1].split('.')[0] + '_contrast.jpg')

    # Create image to draw sunlit areas.  This will become the output sunlight map
    sunMap = Image.new("L", imgBW.size, 255)

    # For each pixelin the mask image, check for sunlight in the enhanced input
    # image.  If sunlight is present, output = 0.  Else output = 255.
    w, h = imgBW.size

    for x in range(w):
        for y in range(h):
            # Get value of mask if available, otherwise set mask value to 0,
            # which will run analysis on the whole image.
            if mask:
                maskV = mask.getpixel((x,y))
            else:
                maskV = 0

            if maskV < 125:
                inputV = imgBW.getpixel((x,y))
                if inputV > v:
                    sunMap.putpixel((x,y), 0)

    # Return sunlight map
    if(show):
        sunMap.show()

    return sunMap


def create_sunlight_map_overlay(img, map, filename):
    inputmap = map.convert("RGBA")
    inputimg = img.convert("RGBA")
    inputData = inputmap.getdata()
    addTransparent = []
    for x in inputData:
        if (x[0] == 255 and x[1] == 255 and x[2] == 255) :
            addTransparent.append((255,255,255,0))

        else:
            addTransparent.append((255,0,0,127))
    inputmap.putdata(addTransparent)
    img.paste(inputmap, (0,0), inputmap)
    img.save(outputPath + '\\' + filename.split('.')[0] + '_overlay.jpg')

main()