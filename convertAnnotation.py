import os
import fileinput

def convertAnnotation(train_path,test_path,output_train_path,output_test_path):
    trainFiles = os.listdir(train_path)
    trainFilesNum = len(os.listdir(train_path))/2

    testFiles = os.listdir(test_path)
    testFilesNum = len(os.listdir(test_path))/2

    train_image_file = []
    train_index_file = []

    test_image_file = []
    test_index_file = []

    os.chdir(train_path)
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.jpg'):
            train_image_file.append("./images/train/" + filename)
        elif filename.endswith(".txt"):
            txt_index_file_path = os.path.join(train_path,filename)
            with open(txt_index_file_path, 'r') as f:
                content = f.read()
                train_index_file.append(content.replace('\n',' '))
            with open(output_train_path, 'w') as f:
                for i in range(0,len(train_image_file)):
                    f.write(train_image_file[i])
                    f.write(' ')
                    f.write(train_index_file[i])
                    f.write("\n")
                f.close()

    os.chdir(test_path)
    for filename in os.listdir(os.getcwd()):
        if filename.endswith('.jpg'):
            test_image_file.append("./images/test/" + filename)
        elif filename.endswith(".txt"):
            txt_index_file_path = os.path.join(test_path,filename)
            with open(txt_index_file_path, 'r') as f:
                content = f.read()
                test_index_file.append(content.replace('\n',' '))
            with open(output_test_path, 'w') as f:
                for i in range(0,len(test_image_file)):
                    f.write(test_image_file[i])
                    f.write(' ')
                    f.write(test_index_file[i])
                    f.write("\n")
                f.close()

    os.chdir("..")

train_path = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\train'
test_path = r'C:\Users\xiao-nan.gan\internProject\padTraining\images\test'
output_train_path = os.path.join(r"C:\Users\xiao-nan.gan\internProject\padTraining\scripts", "train.txt")
output_test_path = os.path.join(r"C:\Users\xiao-nan.gan\internProject\padTraining\scripts", "test.txt")
convertAnnotation(train_path,test_path,output_train_path,output_test_path)