import imageio
import imgaug as ia
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import os
import fileinput
# %matplotlib inline
ia.seed(1)

def getBBlist(imgpath):
    pre,ext = os.path.splitext(imgpath)
    txtpath = pre +'.txt'
    number = []
    output = []
    bbList = []
    with open(txtpath, 'r') as f:
        content = f.read()
        content = content.replace("PAD",'0')
        for x in content:
            if x == ',':
                number = int("".join(number))
                output.append(number)
                number = []

            elif x == "\n":
                bbList.append(output)
                number = []
                output = []
            else:
                number.append(x)
    return bbList
    
imgPath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\train\4_1_1_1.jpg'

image = imageio.imread(imgPath)
image = ia.imresize_single_image(image, (1024, 1024))

bbList = getBBlist(imgPath)


bbs = BoundingBoxesOnImage([
    BoundingBox(x1=bbList[x][0], x2=bbList[x][2], y1=bbList[x][1], y2=bbList[x][3]) for x in range(len(bbList))
], shape=image.shape)

ia.imshow(bbs.draw_on_image(image, size=2))

