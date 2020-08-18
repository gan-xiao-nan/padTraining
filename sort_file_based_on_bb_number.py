import os
from random import shuffle
from math import floor
from os import listdir
import shutil

def getBBlist(img_path):
    pre,ext = os.path.splitext(img_path)
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

imageFolderPath = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\test'
for filename in os.listdir(imageFolderPath):
    if filename.endswith('.jpg'):
        img_path = os.path.join(imageFolderPath,filename)
        bbList = getBBlist(img_path)
        prefilename, file_extension = os.path.splitext(img_path)
        txt_path = prefilename+'.txt'
        print('txtpath = ',txt_path)

        if len(bbList) < 2:
            pass
        elif len(bbList) < 4:
            des_folder_path = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\beforeAugmentation\sorted2'
            des_img_path = os.path.join(des_folder_path,filename)
            prefilename, file_extension = os.path.splitext(des_img_path)
            des_txt_path = prefilename + '.txt'
            print('despath = ',des_img_path,des_txt_path)
            shutil.copyfile(img_path, des_img_path)
            shutil.copyfile(txt_path, des_txt_path)

        elif len(bbList) < 8:
            des_folder_path = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\beforeAugmentation\sorted4'
            des_img_path = os.path.join(des_folder_path,filename)
            prefilename, file_extension = os.path.splitext(des_img_path)
            des_txt_path = prefilename + '.txt'
            print('despath = ',des_img_path,des_txt_path)
            shutil.copyfile(img_path, des_img_path)
            shutil.copyfile(txt_path, des_txt_path)

        elif len(bbList) < 16:
            des_folder_path = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\beforeAugmentation\sorted8'
            des_img_path = os.path.join(des_folder_path,filename)
            prefilename, file_extension = os.path.splitext(des_img_path)
            des_txt_path = prefilename + '.txt'
            print('despath = ',des_img_path,des_txt_path)
            shutil.copyfile(img_path, des_img_path)
            shutil.copyfile(txt_path, des_txt_path)

        elif len(bbList) < 32:
            des_folder_path = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\beforeAugmentation\sorted16'
            des_img_path = os.path.join(des_folder_path,filename)
            prefilename, file_extension = os.path.splitext(des_img_path)
            des_txt_path = prefilename + '.txt'
            print('despath = ',des_img_path,des_txt_path)
            shutil.copyfile(img_path, des_img_path)
            shutil.copyfile(txt_path, des_txt_path)

        elif len(bbList) >= 32:
            des_folder_path = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\beforeAugmentation\sorted32'
            des_img_path = os.path.join(des_folder_path,filename)
            prefilename, file_extension = os.path.splitext(des_img_path)
            des_txt_path = prefilename + '.txt'
            print('despath = ',des_img_path,des_txt_path)
            shutil.copyfile(img_path, des_img_path)
            shutil.copyfile(txt_path, des_txt_path)