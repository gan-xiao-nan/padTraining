import os
import fileinput
import numpy as np
import cv2
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

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

from scipy import spatial

def findNearest(bbList,k = 1):
    neighbours = []
    tree = spatial.KDTree(bbList)
    for x in range(len(bbList)):
        dupBBlist = bbList.copy()
        # delete itself from the list, else shortest distance will always 0 (compare with itself)
        if int(tree.query((dupBBlist[x][0],dupBBlist[x][1],dupBBlist[x][2],dupBBlist[x][3]))[0]) is 0:
            del dupBBlist[x]
        
        if len(dupBBlist) is not x:
            print(tree.query((dupBBlist[x][0],dupBBlist[x][1],dupBBlist[x][2],dupBBlist[x][3])))
            neighbours.append(tree.query((dupBBlist[x][0],dupBBlist[x][1],dupBBlist[x][2],dupBBlist[x][3]))[1])
    return neighbours




imgpath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\train\4_1_1_1.jpg'
image = cv2.imread(imgpath)
#bbList = getBBlist(imgpath)
bbList = [[1,1,1,1],[2,2,2,2],[3,3,3,3]]
totalBB = len(bbList)
print('result is ' ,findNearest(bbList,1))



