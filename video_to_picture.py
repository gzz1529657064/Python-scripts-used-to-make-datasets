import cv2
vc = cv2.VideoCapture('E:/HDV-2019-5-8/Movie/20190508_0095.MP4') 
c=0
rval=vc.isOpened()
timeF = 30
while rval:   
    c = c + 1
    rval, frame = vc.read()
    if (c % timeF == 0):
        cv2.imwrite('E:/HDV-2019-5-8/digital_light/95/'+str(c).zfill(8) + '.jpg', frame)	
    cv2.waitKey(1)

vc.release()