import os
import fileinput
import knn_imgaug as myFunction


def imgaug(imageFolderPath,n_neighbor):
    #outputFolderPath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\afterAugmentation\imgaug' + str(n_neighbor)
    outputFolderPath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\afterAugmentation\imgaug' + str(2)
    print('input',imageFolderPath)
    print('output',outputFolderPath)
    for filename in os.listdir(imageFolderPath):
        if filename.endswith('.jpg'):
            imgpath = os.path.join(imageFolderPath,filename)
            print('imgpath = ',imgpath)
            myFunction.knn_imgaug(imgpath,outputFolderPath,n_neighbor)
    imageFolderPath = outputFolderPath

imageFolderPath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\test'
n_neighbors = [32,16,8,4,2]

# To run 32 - 16 - 8 - 4 -2 in one click
# for n_neighbor in n_neighbors:
#     imgaug(imageFolderPath,n_neighbor)

#To run separately for each n_neighbor
imgaug(imageFolderPath,n_neighbor=2)
