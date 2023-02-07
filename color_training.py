import cv2
import numpy as np
print(cv2.__version__)
height=360
width=640
cam=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FPS,30)
cam.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

def onTrack1(val):
    global hueLow
    hueLow=val
    return hueLow
def onTrack2(val):
    global hueHigh
    hueHigh=val
    return hueHigh
def onTrack3(val):
    global satLow
    satLow=val
    return satLow
def onTrack4(val):
    global satHigh
    sathigh=val
    return satHigh
def onTrack5(val):
    global valLow
    valLow=val
    return valLow
def onTrack6(val):
    global valHigh
    valHigh=val
    return valHigh

hueLow=10
hueHigh=20
satLow=10
satHigh=255
valLow=10
valHigh=255

cv2.namedWindow('My Trackbar')
cv2.moveWindow('My Trackbar',width,0)
cv2.createTrackbar('Hue Low','My Trackbar',10,180,onTrack1)
cv2.createTrackbar('Hue High','My Trackbar',20,180,onTrack2)
cv2.createTrackbar('Sat Low','My Trackbar',10,255,onTrack3)
cv2.createTrackbar('Sat High','My Trackbar',10,255,onTrack4)
cv2.createTrackbar('Val Low','My Trackbar',10,255,onTrack5)
cv2.createTrackbar('Val High','My Trackbar',10,255,onTrack6)

while True:
    ignore, frame=cam.read()
    frameHSV=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lowerBound=np.array([hueLow,satLow,valLow])
    upperBound=np.array([hueHigh,satHigh,valHigh])
    myMask=cv2.inRange(frameHSV,lowerBound,upperBound)
    myMaskSmall=cv2.resize(myMask,(int(width/2),int(height/2)))
    cv2.imshow('My mask',myMaskSmall)
    cv2.moveWindow('My mask',0,height+30)
    contours,junk=cv2.findContours(myMask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area=cv2.contourArea(contour)
        if area>200:
            x,y,w,h=cv2.boundingRect(contour)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
    cv2.imshow('myWEBCAM',frame)
    cv2.moveWindow('myWEBCAM',0,0)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cam.release()
print('My lower Bound is {}:'.format(lowerBound))
print('My upper Bound is {}:'.format(upperBound))
cv2.destroyAllWindows()