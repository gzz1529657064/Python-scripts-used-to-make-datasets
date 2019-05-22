
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
