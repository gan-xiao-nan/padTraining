import os
import fileinput
import numpy as np
import cv2
from itertools import combinations
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
    myCombination = list(combinations(bbList,k))
    random.shuffle(myCombination)
    return myCombination

#     # output = sum([list(map(list,)) ], [])
#     outputs=[]
#     for i in range(len(bbList), len(bbList) + 1):
#         output  =  list(combinations(bbList, i)) 
#         output = shuffle(output)
#         count = 0 
#         for e in output:
#             #Cal box
#             #How many box in big box
#             #More than i??
#             #Drop
#             #Else 
#             #   outputs.append(e6)
#             #   count++
#             # if count>=k
#             # break
            
#         #Drop invalid
#         outputs.append(output)
        

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

    elif((x_min<=x_min_bb) and (x_max>=x_max_bb)):
        inside = (y_min in [i for i in range(y_min_bb,y_max_bb)]) | (y_max in [i for i in range(y_min_bb,y_max_bb)])
        return inside
    elif((y_min<=y_min_bb) and (y_max>=y_max_bb)):
        inside = (y_min in [i for i in range(y_min_bb,y_max_bb)]) | (y_max in [i for i in range(y_min_bb,y_max_bb)])
        return inside
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

    end = time.time()-start
    print('time of dropBB = ',end)
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
    r1 = random.randint(5,50)
    r2 = random.randint(5,50)
    r3 = random.randint(5,50)
    r4 = random.randint(5,50)
    print(r1,r2,r3,r4)
    border = np.zeros((image.shape[0]+r3+r4,image.shape[1]+r1+r2,3))
    print('border.shape',border.shape)
    print(r3,image.shape[0]+r3)
    print(r1,(image.shape[1]+r1))
    border[r3:(image.shape[0]+r3),r1:(image.shape[1]+r1),0:3] = image
    return r1,r2,r3,r4,border

def newBBCoor(small,big,r1,r3):
    [x_min,y_min,x_max,y_max] = small
    [x_min_bb,x_max_bb,y_min_bb,y_max_bb] = big
    x_min_new = x_min - x_min_bb +r1
    y_min_new = y_min - y_min_bb +r3
    x_max_new = x_max - x_min_bb +r1
    y_max_new = y_max - y_min_bb +r3
    return [x_min_new,y_min_new,x_max_new,y_max_new]

imgpath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\train\4_1_1_1.jpg'
image = cv2.imread(imgpath)
bbList = getBBlist(imgpath)
k = 2
myCombination = nCrList(bbList,k)
bigBB = findBigBB(myCombination,k)
final,myDict = dropBB(bigBB,bbList,k)

outputFolderPath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\imgaug'

# for x in range(len(final)):
#     [x_min_bb,y_min_bb,x_max_bb,y_max_bb] = final[x]
#     cropped = image[y_min_bb:y_max_bb,x_min_bb:x_max_bb]    
#     r1,r2,r3,r4,output = addBorder(cropped)
#     filename = 'cropped'+str(x)+'.jpg'
#     outputFileName = os.path.join(outputFolderPath,filename)
#     cv2.imwrite(outputFileName,output)
    # for j in range(k):
    #     min_new,y_min_new,x_max_new,y_max_new] = newBBCoor(myCombination[],final[x],r1,r3)

for x,index in enumerate(myDict,0):
    [x_min_bb,y_min_bb,x_max_bb,y_max_bb] = final[x]
    cropped = image[y_min_bb:y_max_bb,x_min_bb:x_max_bb]    
    r1,r2,r3,r4,output = addBorder(cropped)
    filename = 'cropped'+str(x)+'.jpg'
    outputFileName = os.path.join(outputFolderPath,filename)
    cv2.imwrite(outputFileName,output)
#     min_new,y_min_new,x_max_new,y_max_new] = newBBCoor(myCombination[],final[x],r1,r3)