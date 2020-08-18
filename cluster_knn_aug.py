from sklearn.neighbors import NearestNeighbors
import numpy as np
import cv2
import os
import random

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

def isOverlap(small,big):
    [x_min,y_min,x_max,y_max] = small
    [x_min_bb,y_min_bb,x_max_bb,y_max_bb] = big
    if (x_min<x_max_bb and x_max>x_min_bb):
        if(y_min<y_max_bb and y_max>y_min_bb):
            return True
        else:
            return False
    else:
        return False

def findBBinside(bbList,bigBB):
    bbInside = []
    for i in range(len(bbList)):
        if isOverlap(bbList[i],bigBB) is True:
            bbInside.append(bbList[i])
    return bbInside

def addBorder(image):
    r_left = random.randint(5,50)
    r_right = random.randint(5,50)
    r_top = random.randint(5,50)
    r_bottom = random.randint(5,50)
    border = np.zeros((image.shape[0]+r_top+r_bottom,image.shape[1]+r_left+r_right,3))
    border[r_top:(image.shape[0]+r_top),r_left:(image.shape[1]+r_left),0:3] = image
    return r_left,r_right,r_top,r_bottom,border

def newBBCoor(small,big,r_top,r_left):
    [x_min,y_min,x_max,y_max] = small
    [x_min_bb,y_min_bb,x_max_bb,y_max_bb] = big
    width_bb = x_max_bb - x_min_bb 
    height_bb = y_max_bb - y_min_bb
    if x_min<=x_min_bb: 
        x_min_new = r_left
    elif x_min > x_min_bb:
        x_min_new = width_bb - (x_max_bb - x_min) + r_left
    if y_min<=y_min_bb: 
        y_min_new = r_top
    elif y_min > y_min_bb:
        y_min_new = height_bb - (y_max_bb - y_min) + r_top
    if x_max >= x_max_bb: 
        x_max_new = width_bb + r_left
    elif x_max < x_max_bb:
        x_max_new = width_bb - (x_max_bb - x_max) + r_left
    if y_max >= y_max_bb: 
        y_max_new = height_bb + r_top
    elif y_max < y_max_bb:
        y_max_new = height_bb - (y_max_bb - y_max) + r_top
    return [x_min_new,y_min_new,x_max_new,y_max_new]    

def writeBBlist(filename,coor_single_cropped_img):
    pre,ext = os.path.splitext(filename)
    txtpath = pre +'.txt'
    # print(txtpath)
    with open(txtpath, 'w') as f:
        for bb_coor in coor_single_cropped_img:
            for coor in bb_coor:
                f.write(str(coor))
                f.write(',')
            f.write('PAD')
            f.write('\n')

def output(image,outputFolderPath,bigBB,bbInside,i):
    big = [x_min_bb,y_min_bb,x_max_bb,y_max_bb] = bigBB
    cropped = image[y_min_bb:y_max_bb,x_min_bb:x_max_bb]
    r_left,r_right,r_top,r_bottom,output = addBorder(cropped)
    coor_single_cropped_img = []
    for k_th in range(len(bbInside)):
        small = [x_min_bb,y_min_bb,x_max_bb,y_max_bb] = bbInside[k_th]
        coor_single_bb = newBBCoor(small,big,r_top,r_left)
        coor_single_cropped_img.append(coor_single_bb)
    filename = outputFolderPath + '\cropped'+str(i)+'.jpg'
    outputFileName = os.path.join(outputFolderPath,filename)
    cv2.imwrite(outputFileName,output)
    writeBBlist(filename,coor_single_cropped_img)

imgpath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\train\4_2_1_4.jpg'
outputFolderPath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\imgaug'
n_neighbors = 32
image = cv2.imread(imgpath)
X = bbList =getBBlist(imgpath)
nbrs = NearestNeighbors(n_neighbors, algorithm='auto').fit(X)
distances, indices = nbrs.kneighbors(X)
myIndices = [indices[i] for i in range(0,len(indices),n_neighbors)]
for i,indice in enumerate(myIndices):
    print('indices = ',indice)
    min_x = 2000
    min_y = 2000
    max_x = 0
    max_y = 0
    for j in indice:
        #find largest bb
        if  bbList[j][0] <= min_x:
            min_x =  bbList[j][0]
        if  bbList[j][1] <= min_y:
            min_y =  bbList[j][1]
        if  bbList[j][2] >= max_x:
            max_x =  bbList[j][2]
        if  bbList[j][3] >= max_y:
            max_y =  bbList[j][3]
        bigBB = [min_x,min_y,max_x,max_y]
    bbInside = findBBinside(bbList,bigBB)
    print('bbInside',bbInside)
    print('lenBBinside',len(bbInside))
    r_left,r_right,r_top,r_bottom,border = addBorder(image)
    output(image,outputFolderPath,bigBB,bbInside,i)
    