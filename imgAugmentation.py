import os
import fileinput
import numpy as np
import cv2
from itertools import combinations
import time

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
    output = sum([list(map(list, combinations(bbList, i))) for i in range(len(bbList) + 1)], [])
    myCombination = [output[x] for x in range(len(output)) if len(output[x]) == k]
    end = time.time()-start
    print('time of find combination = ',end)
    return myCombination

def findBigBB(myCombination,k):
    print('finding big bounding box')
    start = time.time()
    bigBB = []
    #find min_x for each combination, store in a list
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
    print('time of find bigBB = ',end)
    return bigBB

def isOverlap(small,big):
    [x_min,y_min,x_max,y_max] = small
    [x_min_bb,y_min_bb,x_max_bb,y_max_bb] = big
    if x_min>=x_min_bb and x_max<=x_max_bb:
        if y_min>=y_min_bb and y_max<=y_max_bb:
            return True
        else:
            return False

    elif(((x_min<=x_min_bb) and (x_max>=x_max_bb)) | ((y_min<=y_min_bb) and (y_max>=y_max_bb))):
        return True
    else:
        return False

def dropBB(bigBB,bbList,k):
    print('dropping bounding box')
    start = time.time()
    boolOut = [[isOverlap(bbList[i],bigBB[j]) for i in range(len(bbList))] for j in range(len(bigBB))]
    #final = [bigBB[i] for i in range(len(boolOut)) if sum(boolOut[i]) is k]
    final = []
    myDict = {i:i for i in range(len(bigBB))}
    for i in range(len(boolOut)):
        print(i)
        if sum(boolOut[i]) is k:
            final.append(bigBB[i])
        else:
            del myDict[i]
    print('myDict','\n',myDict)  
    print('problem set\n')
    print('bigBB\n',bigBB[23])
    print('isOverlap\n',boolOut[23])

    end = time.time()-start
    print('time of dropBB = ',end)
    return final

def drawBBonImage(bigBBindex,myCombination,image,imgpath,k):
    for x in bigBBindex.values():
        image = cv2.imread(imgpath)
        for y in range(k):
            a = int(myCombination[x][y][0])
            b = int(myCombination[x][y][1])
            c = int(myCombination[x][y][2])
            d = int(myCombination[x][y][3])
            cv2.rectangle(image, (a,b), (c,d), (0,255,0),2)
        # cv2.imshow('t',image) 
        # cv2.waitKey(1000)   
        image = original

imgpath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\train\49043Bottom_6_3_7.jpg'
image = cv2.imread(imgpath)
bbList = getBBlist(imgpath)
k = 4
myCombination = nCrList(bbList,k)
bigBB = findBigBB(myCombination,k)
final = dropBB(bigBB,bbList,k)
outputFolderPath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\imgaug'
# # drawBBonImage(bigBBindex,myCombination,image,imgpath,k)
for x in range(len(final)):
    [x_min_bb,y_min_bb,x_max_bb,y_max_bb] = final[x]
    cropped = image[y_min_bb:y_max_bb,x_min_bb:x_max_bb]    
    filename = 'cropped'+str(x)+'.jpg'
    outputFileName = os.path.join(outputFolderPath,filename)
    cv2.imwrite(outputFileName,cropped)

cv2.rectangle(image, (1,1), (23,899), (0,255,0),2)
image = cv2.resize(image, (416,416), interpolation = cv2.INTER_AREA)
cv2.imshow('i',image)

cv2.waitKey(0)