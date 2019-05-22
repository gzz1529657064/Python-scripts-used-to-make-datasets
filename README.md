# Python-scripts-used-to-make-datasets
最近一直在做图片数据集，积累了很多心得。我把我所使用的python脚本全部拿出来，当然这些脚本大部分网上都有，只不过比较分散。

由于我的数据集是在拍摄路面的一些物体。因此分为视频和图片两种。视频分辨率1920x1080，帧率为60fps，图片分辨率为1920x1080。光拍摄图片比较慢，拍摄视频获取图片速度很快，毕竟可以将视频分解成帧，这样就可以在短时间内获取大量图片。顺便说一句，录制视频的时候可以缓慢的上下、左右移动镜头，这样得到的图片数据比较丰富。不是那种高度重复的

1. 视频分解为帧 video_to_picture.py
import cv2
vc = cv2.VideoCapture('E:/HDV-2019-5-8/Movie/20190508_0095.MP4') 
c=0
rval=vc.isOpened()
timeF = 30
while rval:   
    c = c + 1
    rval, frame = vc.read()
    if (c % timeF == 0):
        cv2.imwrite('E:/HDV-2019-5-8/digital_light/95/'+str(c).zfill(5) + '.jpg', frame)    
    cv2.waitKey(1)

vc.release()
其中 timeF 表示帧率，你也可以改小一点。一秒中获取2帧到4帧左右；zfill(5)：表示图片从00000~99999，数字的位数。如果视频很长，可以把5调大一点。

 

2. 手动删除不需要的图片
 

3. 按照VOC数据集的格式。详情请看我上篇博客 : 在Ubuntu内制作自己的VOC数据集
 

4. 把所有图片放入JPEGImages文件中，后缀名一般为 .jpg .png .JPG。需要批量重命名文件夹中图片文件。使用rename.py
# -*- coding:utf8 -*-
 
import os
class BatchRename():
    '''
    批量重命名文件夹中的图片文件
    '''
    def __init__(self):
        self.path = '/home/z/work/train'     #存放图片的文件夹路径
    def rename(self):
        filelist = os.listdir(self.path)
        total_num = len(filelist)
        i = 1
        for item in filelist:
            if item.endswith('.jpg') or item.endswith('.JPG'):  #图片格式为jpg、JPG
 
                src = os.path.join(os.path.abspath(self.path), item)
                dst = os.path.join(os.path.abspath(self.path), str(i).zfill(5) + '.jpg')      #设置新的图片名称
                try:
                    os.rename(src, dst)
                    print ("converting %s to %s ..." % (src, dst))
                    i = i + 1        
                except:
                    continue
 
        print ("total %d to rename & converted %d jpgs" % (total_num, i))
if __name__ == '__main__':
    demo = BatchRename()
 
    demo.rename()
只需要修改图片路径、增添图片格式、zfill(5)表示图片名称从00001~99999，可以按照自己的图片数量进行修改。

 

5. 使用labelImg进行标注。标注是一个非常漫长而又无聊的过程，坚持住！
每个图片都会产生一个xml文件。

 
6. 检查xml文件。check_annotations.py
import os
def getFilePathList(dirPath, partOfFileName=''):
    allFileName_list = list(os.walk(dirPath))[0][2]
    fileName_list = [k for k in allFileName_list if partOfFileName in k]
    filePath_list = [os.path.join(dirPath, k) for k in fileName_list]
    return filePath_list


def check_1(dirPath):
    jpgFilePath_list = getFilePathList(dirPath, '.jpg')
    allFileMarked = True
    for jpgFilePath in jpgFilePath_list:
        xmlFilePath = jpgFilePath[:-4] + '.xml'
        if not os.path.exists(xmlFilePath):
            print('%s this picture is not marked.' %jpgFilePath)
            allFileMarked = False
    if allFileMarked:
        print('congratulation! it is been verified that all jpg file are marked.')

       
import xml.etree.ElementTree as ET
def check_2(dirPath, className_list):
    className_set = set(className_list)
    xmlFilePath_list = getFilePathList(dirPath, '.xml')
    allFileCorrect = True
    for xmlFilePath in xmlFilePath_list:
        with open(xmlFilePath, 'rb') as file:
            fileContent = file.read()
        root = ET.XML(fileContent)
        object_list = root.findall('object')
        for object_item in object_list:
            name = object_item.find('name')
            className = name.text
            if className not in className_set:
                print('%s this xml file has wrong class name "%s" ' %(xmlFilePath, className))
                allFileCorrect = False
    if allFileCorrect:
        print('congratulation! it is been verified that all xml file are correct.')

if __name__ == '__main__':
    dirPath = 'Picture/'
    className_list = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]    
    check_1(dirPath)
    check_2(dirPath, className_list)
 此时图片和xml在一个文件夹下。文件夹名称为dirPath。

两个功能：1. 是否有图片漏标。2. 标注的类别是否有拼写错误。在className_list中填写正确的所有类别。

如果存在漏标、类别拼写错误，会打印出图片的名称。

 

7. 如果出现大数量的类别拼写错误。比如：行人（pedestrian）拼写成 pedestrain。可以使用replace_xml_label.py
# coding=utf-8
import os
import os.path
import xml.dom.minidom
 
path = 'Annotations'
files = os.listdir(path)
s = []
for xmlFile in files:
    portion = os.path.splitext(xmlFile)
    if not os.path.isdir(xmlFile):
 
        dom = xml.dom.minidom.parse(os.path.join(path, xmlFile))

        root = dom.documentElement
        name = root.getElementsByTagName('name')

        for i in range(len(name)):
            if name[i].firstChild.data == 'pedestrain':
                name[i].firstChild.data = 'pedestrian'
    with open(os.path.join(path, xmlFile), 'w', encoding='UTF-8') as fh:
        dom.writexml(fh)
        print('replace filename OK!')
 

8. 获取每个类的数目，查看数据是否平衡。 getClasses.py
import os
import xml.etree.ElementTree as ET
import numpy as np

np.set_printoptions(suppress=True, threshold=np.nan)
import matplotlib
from PIL import Image


def parse_obj(xml_path, filename):
    tree = ET.parse(xml_path + filename)
    objects = []
    for obj in tree.findall('object'):
        obj_struct = {}
        obj_struct['name'] = obj.find('name').text
        objects.append(obj_struct)
    return objects


def read_image(image_path, filename):
    im = Image.open(image_path + filename)
    W = im.size[0]
    H = im.size[1]
    area = W * H
    im_info = [W, H, area]
    return im_info


if __name__ == '__main__':
    xml_path = 'Annotations/'
    filenamess = os.listdir(xml_path)
    filenames = []
    for name in filenamess:
        name = name.replace('.xml', '')
        filenames.append(name)
    recs = {}
    obs_shape = {}
    classnames = []
    num_objs = {}
    obj_avg = {}
    for i, name in enumerate(filenames):
        recs[name] = parse_obj(xml_path, name + '.xml')
    for name in filenames:
        for object in recs[name]:
            if object['name'] not in num_objs.keys():
                num_objs[object['name']] = 1
            else:
                num_objs[object['name']] += 1
            if object['name'] not in classnames:
                classnames.append(object['name'])
    for name in classnames:
        print('{}:{}个'.format(name, num_objs[name]))
    print('信息统计算完毕。')
 

9. 生成ImageSets\Main文件夹下的4个txt文件：test.txt，train.txt，trainval.txt，val.txt
这四个文件存储的是上一步xml文件的文件名。trainval和test内容相加为所有xml文件，train和val内容相加为trainval。使用CreateTxt.py生成。要将该文件与ImageSets和Annotations放在同一目录下

import os
import random

trainval_percent = 0.8  # trainval数据集占所有数据的比例
train_percent = 0.5  # train数据集占trainval数据的比例
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
 

10. 将test.txt，train.txt，trainval.txt，val.txt转化为下面这种格式。使用voc_annotation.py
路径 类别名 xmin ymin xmax ymax

例如：

xxx/xxx/a.jpg 0 453 369 473 391 1 588 245 608 268

xxx/xxx/b.jpg 1 466 403 485 422 2 793 300 809 320

import xml.etree.ElementTree as ET
from os import getcwd

sets=[('2018', 'train'), ('2018', 'val'), ('2018', 'test'), ('2018', 'trainval')]

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]


def convert_annotation(year, image_id, list_file):
    in_file = open('VOCdevkit\VOC%s\Annotations\%s.xml'%(year, image_id), encoding = 'utf-8')
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        #list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
        list_file.write(" " + str(cls_id) + ' ' + " ".join([str(a) for a in b]))

wd = getcwd()

for year, image_set in sets:
    image_ids = open('VOCdevkit\VOC%s\ImageSets\Main\%s.txt'%(year, image_set)).read().strip().split()
    list_file = open('%s_%s.txt'%(year, image_set), 'w')
    for image_id in image_ids:
        list_file.write('%s\VOCdevkit\VOC%s\JPEGImages\%s.jpg'%(wd, year, image_id))
        convert_annotation(year, image_id, list_file)
        list_file.write('\n')
        
    list_file.close()
同样地在classes里面填写你自己实际的类别。

如果碰到图片输入是这样：路径 xmin ymin xmax ymax 类别名。将代码中标红的部分调换一下顺序即可

list_file.write(" " + " ".join([str(a) for a in b]) + ' ' + str(cls_id))
 

总结
后面可能还会有将图片制作成 tfrecord文件用于tensorflow训练，lmdb文件用于caffe训练。脚本会继续增加。

 
