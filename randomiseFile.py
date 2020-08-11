import os
from random import shuffle
from math import floor
from os import listdir
import shutil

def randomize_files(file_list):
    shuffle(file_list)

def randomise(src_folder_path):
    all_files = os.listdir(os.path.abspath(src_folder_path))
    files = list(filter(lambda file: file.endswith('.jpg'), all_files))
    shuffle(files)
    train, test = get_training_and_testing_sets(files)
    return train,test

def get_training_and_testing_sets(file_list):
    split = 0.8
    split_index = floor(len(file_list) * split)
    training = file_list[:split_index]
    testing = file_list[split_index:]
    return training, testing

def write_to_file(src_folder_path,des_folder_path,train_or_test_list):
    for filename in train_or_test_list:
        img_path = os.path.join(src_folder_path,filename)
        print(img_path)

        prefilename, file_extension = os.path.splitext(img_path)
        txt_path = prefilename+'.txt'
        print('txtpath = ',txt_path)

        des_img_path = os.path.join(des_folder_path,filename)
        prefilename, file_extension = os.path.splitext(des_img_path)
        des_txt_path = prefilename + '.txt'
        print('despath = ',des_img_path,des_txt_path)

        shutil.move(img_path, des_img_path)
        shutil.move(txt_path, des_txt_path)
        # shutil.copyfile(img_path, des_img_path)
        # shutil.copyfile(txt_path, des_txt_path)
        

train,test = randomise(r'C:\Users\xiao-nan.gan\internProject\padTraining\images')
write_to_file(r'C:\Users\xiao-nan.gan\internProject\padTraining\images',r'C:\Users\xiao-nan.gan\internProject\padTraining\images\test',test)
write_to_file(r'C:\Users\xiao-nan.gan\internProject\padTraining\images',r'C:\Users\xiao-nan.gan\internProject\padTraining\images\train',train)


