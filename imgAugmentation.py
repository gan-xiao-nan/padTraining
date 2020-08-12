import os
import fileinput
import numpy as np
import cv2
from scipy import spatial
from itertools import combinations
# %matplotlib inline

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
    print('shape',len(output))
    myCombination = []
    for x in range(len(output)):
        if len(output[x]) is k:
            myCombination.append(output[x])
        else:
            pass
    return myCombination

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

def findNearest(bbList,k_neighbour):
    neighbours = []
    neighbour = []
    tree = spatial.KDTree(bbList)

    for x in range(len(bbList)):
        dupBBlist = bbList.copy()
        # delete itself from the list, else shortest distance will always 0 (compare with itself)
        if int(tree.query((dupBBlist[x][0],dupBBlist[x][1],dupBBlist[x][2],dupBBlist[x][3]))[0]) is 0:
            del dupBBlist[x]
            noTargetList = dupBBlist
        
        if len(noTargetList) is not x:
            (shortestDist,dup_ind) = tree.query((noTargetList[x][0],noTargetList[x][1],noTargetList[x][2],noTargetList[x][3]))
            neighbour.append(dup_ind)
    neighbours.append(neighbour)
    return noTargetList, neighbours




imgpath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\train\4_1_1_1.jpg'
image = cv2.imread(imgpath)



bbList = getBBlist(imgpath)
# output = sum([list(map(list, combinations(bbList, i))) for i in range(len(bbList) + 1)], [])
# print(type(output),len(output))
# print(output[0])
# print(output[1])
# print(output[2])



myCombination = nCrList(bbList,3)
print(myCombination)
# print(type(myCombination))
# print(len(myCombination))
def findBigBB(myCombination,k):
    min_x_list = []
    min_y_list = []
    max_x_list = []
    max_y_list = []
    bigBB = []

    #find min_x for each combination, store in a list
    for x in range(len(myCombination)):
        min_x = 2000
        for y in range(k):
            if myCombination[x][y][0] <= min_x:
                min_x = myCombination[x][y][0]
        min_x_list.append(min_x)

    #find min_y for each combination, store in a list
    for x in range(len(myCombination)):
        min_y = 2000
        for y in range(k):
            if myCombination[x][y][1] <= min_y:
                min_y = myCombination[x][y][1]
        min_y_list.append(min_y)

    #find max_x for each combination, store in a list
    for x in range(len(myCombination)):
        max_x = 0
        for y in range(k):
            if myCombination[x][y][2] >= max_x:
                max_x = myCombination[x][y][2]
        max_x_list.append(max_x)

    #find max_y for each combination, store in a list
    for x in range(len(myCombination)):
        max_y = 2000
        for y in range(k):
            if myCombination[x][y][3] <= max_y:
                max_y = myCombination[x][y][3]
        max_y_list.append(max_y)
    
    # for each combination, arrange coordinate into ((x_min,y_min,x_max,y_max),(x_min,y_min,x_max,y_max),...)
    for x in range(len(myCombination)):
        # 4 is number of coordinate in each single list (x_min,y_min,x_max,y_max)
        bigBB.append(min_x_list[x])
        bigBB.append(min_y_list[x])
        bigBB.append(max_x_list[x])
        bigBB.append(max_y_list[x])
    return bigBB

# a,b,c,d = findBigBB(myCombination,3)
# print(a)
# print(len(a))
# print(len(myCombination))
# print(a[83])
print(findBigBB(myCombination,3))