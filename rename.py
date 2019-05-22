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