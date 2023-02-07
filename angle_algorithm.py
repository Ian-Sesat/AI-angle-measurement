import cv2
import numpy as np
print(cv2.__version__)
width=640
height=360
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

color1LowerBound=np.array([50,95,113])
color1UpperBound=np.array([92,255,255])
color2LowerBound=np.array([96,156,219])
color2UpperBound=np.array([120,255,255])
x1=0
y1=0
x0=0
y0=0

def calculateAngle(x0,y0,x1,y1):
    b=x1-x0
    h=y1-y0
    if b==0:
        b=1
    if h==0:
        h=1
    angle=np.arctan(h/b)
    angle=np.rad2deg(angle)
    return angle

while True:
    ignore, frame=cam.read()
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    myMask1=cv2.inRange(frameHSV,color1LowerBound,color1UpperBound)
    myMask2=cv2.inRange(frameHSV,color2LowerBound,color2UpperBound)
    contours1,junk=cv2.findContours(myMask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours1:
        area=cv2.contourArea(contour)
        if area>200:
            x,y,w,h=cv2.boundingRect(contour)
            x0=x+int(w/2)
            y0=y+int(h/2)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)          
    contours2,junk=cv2.findContours(myMask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for cntr in contours2:
        area2=cv2.contourArea(cntr)
        if area2>200:
            x2,y2,w2,h2=cv2.boundingRect(cntr)
            x1=x2+int(w2/2)
            y1=y2+int(h2/2)
            cv2.rectangle(frame,(x2,y2),(x2+w2,y2+h2),(0,255,0),2)
    angle=calculateAngle(x0,y0,x1,y1)
    print(angle)
    cv2.imshow('My Camera',frame)
    if cv2.waitKey(1)&0xff==ord('q'):
        break

cam.release()
cv2.destroyAllWindows()