import os

from PIL import Image

inputPath = r'C:\Users\danie\Documents\Python\Sunlighttest\Test2'

imgs = [file for file in os.listdir(inputPath) if '.' in file and file.split('.')[1].lower() == 'jpg']

for img in imgs:
    print('Resizing {}...'.format(img))
    input = Image.open(inputPath + '\\' + img)
    w, h = (int(input.width / 4), int(input.height / 4))
    print(w,h)
    input = input.resize((w,h))
    input.save(inputPath + '\\' + img)

print('done')