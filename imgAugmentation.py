import os
import fileinput
import numpy as np
import cv2
from itertools import combinations, islice
import time
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

def nCrList(bbList, k):
    print('building combination ...\n')
    start = time.time()
    # random.shuffle(bbList)
    myCombination = list(islice(combinations(bbList,k), 500000))
    
    random.shuffle(myCombination)
    end = time.time()-start
    print(end)
    return myCombination

def findBigBB(myCombination,k):
    print('finding big bounding box...')
    start = time.time()
    bigBB = []
    print(len(myCombination))
    for x in range(len(myCombination)):
        min_x = 2000
        min_y = 2000
        max_x = 0
        max_y = 0
        for y in range(k):
            if myCombination[x][y][0] <= min_x:
                min_x = myCombination[x][y][0]
            if myCombination[x][y][1] <= min_y:
                min_y = myCombination[x][y][1]
            if myCombination[x][y][2] >= max_x:
                max_x = myCombination[x][y][2]
            if myCombination[x][y][3] >= max_y:
                max_y = myCombination[x][y][3]
        bigBB.append([min_x,min_y,max_x,max_y])
    end = time.time()-start
    print(end)
    return bigBB

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

def dropBB(bigBB,bbList,k):
    print('Dropping invalid bb...')
    start = time.time()
    boolOut = [[isOverlap(bbList[i],bigBB[j]) for i in range(len(bbList))] for j in range(len(bigBB))]
    final = []
    myDict = {i:i for i in range(len(bigBB))}
    for i in range(len(boolOut)):
        if sum(boolOut[i]) is k:
            final.append(bigBB[i])
        else:
            del myDict[i]
    end = time.time()-start
    print(end)
    return final,myDict

def drawBBonImage(bigBBindex,myCombination,image,imgpath,k):
    for x in bigBBindex.values():
        image = cv2.imread(imgpath)
        for y in range(k):
            a = int(myCombination[x][y][0])
            b = int(myCombination[x][y][1])
            c = int(myCombination[x][y][2])
            d = int(myCombination[x][y][3])
            cv2.rectangle(image, (a,b), (c,d), (0,255,0),2) 
        image = original

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
    x_min_new = width_bb - (x_max_bb - x_min) + r_left
    y_min_new = height_bb - (y_max_bb - y_min) + r_top
    x_max_new = width_bb - (x_max_bb - x_max) + r_left
    y_max_new = height_bb - (y_max_bb - y_max) + r_top
    return [x_min_new,y_min_new,x_max_new,y_max_new]    

def writeBBlist(filename,coor_single_cropped_img):
    pre,ext = os.path.splitext(filename)
    txtpath = pre +'.txt'
    print(txtpath)
    with open(txtpath, 'w') as f:
        for bb_coor in coor_single_cropped_img:
            for coor in bb_coor:
                f.write(str(coor))
                f.write(',')
            f.write('PAD')
            f.write('\n')

imgpath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\train\4_1_2_1.jpg'
image = cv2.imread(imgpath)
bbList = getBBlist(imgpath)
k = 2
myCombination = nCrList(bbList,k)
bigBB = findBigBB(myCombination,k)
final,myDict = dropBB(bigBB,bbList,k)

outputFolderPath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\imgaug'

for x,index in enumerate(myDict,0):
    [x_min_bb,y_min_bb,x_max_bb,y_max_bb] = final[x]
    cropped = image[y_min_bb:y_max_bb,x_min_bb:x_max_bb]    
    r_left,r_right,r_top,r_bottom,output = addBorder(cropped)
    big = final[x]
    coor_single_cropped_img = []
    for k_th in range(k):
        small = myCombination[index][k_th]
        coor_single_bb = newBBCoor(small,big,r_top,r_left)
        coor_single_cropped_img.append(coor_single_bb)
        
    filename = outputFolderPath + '\cropped'+str(x)+'.jpg'
    outputFileName = os.path.join(outputFolderPath,filename)
    cv2.imwrite(outputFileName,output)
    writeBBlist(filename,coor_single_cropped_img)