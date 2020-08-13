import os
import fileinput
import numpy as np
import cv2
from itertools import combinations

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
    output = sum([list(map(list, combinations(bbList, i))) for i in range(len(bbList) + 1)], [])
    myCombination = []
    for x in range(len(output)):
        if len(output[x]) is k:
            myCombination.append(output[x])
        else:
            pass
    return myCombination

def findBigBB(myCombination,k):
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
    return bigBB

def dropOverlap(bigBB,bbList,k):
    count = 0
    final = []
    bigBBindex = {str(i):i for i in range(len(bigBB)) }
    for x in range(len(bigBB)):
        for y in range (len(bbList)):
            if (bigBB[x][0]<=bbList[y][0] and bigBB[x][1]<=bbList[y][1]):
                if (bigBB[x][2]>=bbList[y][2] and bigBB[x][3]>=bbList[y][3]):
                    count += 1
            if count > k:
                del bigBBindex[str(x)]
                count = 0
                break
    for x in bigBBindex.values():
        final.append(bigBB[x])
    return final,bigBBindex

def drawBBonImage(bigBBindex,myCombination,image,imgpath,k):
    for x in bigBBindex.values():
        image = cv2.imread(imgpath)
        for y in range(k):
            a = int(myCombination[x][y][0])
            b = int(myCombination[x][y][1])
            c = int(myCombination[x][y][2])
            d = int(myCombination[x][y][3])
            cv2.rectangle(image, (a,b), (c,d), (0,255,0),2)
        cv2.imshow('t',image) 
        cv2.waitKey(1000)   
        image = original

imgpath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\train\4_1_1_1.jpg'
image = cv2.imread(imgpath)
original = image.copy()
bbList = getBBlist(imgpath)

#print(bbList,len(bbList))
k = 3
myCombination = nCrList(bbList,k)
bigBB = findBigBB(myCombination,k)
bigBB,bigBBindex = dropOverlap(bigBB,bbList,k)
outputFolderPath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\imgaug'
drawBBonImage(bigBBindex,myCombination,image,imgpath,k)
for x in range(len(bigBB)):
    cropped = image[bigBB[x][1]:bigBB[x][3],bigBB[x][0]:bigBB[x][2]]
    filename = 'cropped'+str(x)+'.jpg'
    outputFileName = os.path.join(outputFolderPath,filename)
    cv2.imwrite(outputFileName,cropped)


# for x in bigBB:
#     a = int(x[0])
#     b = int(x[1])
#     c = int(x[2])
#     d = int(x[3])
#     print(a,b,c,d)
#     cv2.rectangle(image, (a,b), (c,d), (0,255,0),2)
# cv2.imshow('image',image)
# cv2.waitKey(0)