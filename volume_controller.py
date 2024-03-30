import cv2
import cvzone
import numpy as np
from time import sleep
import math
import time
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
from cvzone.HandTrackingModule import HandDetector

ptime=0
detector=HandDetector(detectionCon=0.8,maxHands=1)
cap=cv2.VideoCapture(0)
hcam=640
wcam=720
cap.set(3,wcam)
cap.set(4,hcam)
devices=AudioUtilities.GetSpeakers()
interface=devices.Activate(IAudioEndpointVolume._iid_,CLSCTX_ALL,None)
volume=cast(interface,POINTER(IAudioEndpointVolume))
volRange=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0,None)
minvol=volRange[0]
maxvol=volRange[1]

while True:
    _,img=cap.read()
    hands,img=detector.findHands(img)
    if hands:
        lmlist=hands[0]['lmList'] 
        bbox=hands[0]['bbox']
        if len(lmlist)!=0:
            x1,y1=lmlist[4][:2]
            x2,y2=lmlist[8][:2]
            cx, cy = (x1+x2)//2,(y1+y2)//2
            cv2.circle(img,(x1,y1),15,(255,0,0),cv2.FILLED)
            cv2.circle(img,(x2,y2),15,(255,0,0),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)
            cv2.circle(img,(cx,cy),15,(255,0,0),cv2.FILLED)
            length=math.hypot(x2-x1,y2-y1)
            vol=np.interp(length,(50,300),(minvol,maxvol))
            # print(int(length),vol) 
            volume.SetMasterVolumeLevel(vol,None)           
            bar_volu=int(np.interp(length,(50,300),(400,150)))
            cv2.rectangle(img,(50,bar_volu),(85,400),(255,0,255),cv2.FILLED)
            cv2.rectangle(img,(50,150),(85,400),(),3)
            print(int(length),bar_volu)
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cvzone.putTextRect(img,f'FPS-{int(fps)}',(30,50),2,2,colorT=(255,255,255),colorR=(255,0,0),border=3,colorB=())
    interrupt = cv2.waitKey(10)
    cv2.imshow("VOLUME-CONTROLLER",img)
    if interrupt & 0xFF == ord('q'):
        break