import os
from PIL import Image

inputDir = r'C:\Users\danie\Documents\Python\Sunlight-Map\test'
inputOverlayDir = r'C:\Users\danie\Documents\Python\Sunlight-Map\test\output'
outputDir = r'C:\Users\danie\Documents\Python\Sunlight-Map\test\sequence'
imgs = [file for file in os.listdir(inputDir) if '.' in file and file.split('.')[1].lower() == 'jpg']

for imgFilename in imgs:
    img = Image.open(inputDir + '\\' + imgFilename)
    imgOverlay = Image.open(inputOverlayDir + '\\' + imgFilename.split('.')[0] + '_overlay.jpg')
    size = (img.width * 2, img.height)
    newImg = Image.new('RGB', size)

    newImg.paste(img, (0,0))
    newImg.paste(imgOverlay, (img.width,0))
    newImg.save(outputDir + '\\' + imgFilename)

print('done')