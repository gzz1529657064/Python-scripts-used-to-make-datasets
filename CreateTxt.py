#!F:\PyCharm-projects
# coding : utf-8
# author : 葛壮壮

import os
import random

trainval_percent = 0.9  # trainval数据集占所有数据的比例
train_percent = 0.9  # train数据集占trainval数据的比例
xmlfilepath = 'Annotations'
txtsavepath = 'ImageSets/Main'
total_xml = os.listdir(xmlfilepath)

num = len(total_xml)
print('total number is ', num)
list = range(num)
tv = int(num * trainval_percent)
print('trainVal number is ', tv)
tr = int(tv * train_percent)
print('train number is ', tr)
print('test number is ', num - tv)
trainval = random.sample(list, tv)
train = random.sample(trainval, tr)

ftrainval = open('ImageSets/Main/trainval.txt', 'w')
ftest = open('ImageSets/Main/test.txt', 'w')
ftrain = open('ImageSets/Main/train.txt', 'w')
fval = open('ImageSets/Main/val.txt', 'w')

for i in list:
    name = total_xml[i][:-4] + '\n'
    if i in trainval:
        ftrainval.write(name)
        if i in train:
            ftrain.write(name)
        else:
            fval.write(name)
    else:
        ftest.write(name)

ftrainval.close()
ftrain.close()
fval.close()
ftest.close()