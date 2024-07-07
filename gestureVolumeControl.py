import cv2
import advanceHandTrackingModule as htm
import time
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, wCam)
pTime = 0
cTime = 0

detector = htm.handDetector(detectionCon=0.7, maxHands=1)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = 0 # volRange[0]
maxVol = 0 # volRane[1]
vol = 0
volBar = 400
volPer = 0
area = 0
colorVol = (255, 0, 0)

while True:
    success, img = cap.read()
    img = detector.findHands(img, True)
    lmList, bBox = detector.findPosition(img, draw=False)
    
    if len(lmList) != 0:

        area = (bBox[2]-bBox[0]) * (bBox[3]-bBox[1]) // 100
        
        #printing index and thumb
        print(lmList[4], lmList[8])
        
        #print area
        print(area)

        if 200<area<1000:
                
            print("observing")
            # to print thumb and index finger
            length, img, pointersInfo = detector.findDistance(4, 8, img)
            #print(length)

            # Hand range 50 - 200
            # Volumn range -65 - 0
            volBar = np.interp(length, [50, 200], [400, 150])
            volPer = np.interp(length, [50, 200], [0, 100])

            # Reduce resolution to make it smoother
            smoothness = 5
            volPer = smoothness * round(volPer/smoothness)

            # Check fingers up
            fingers = detector.fingersUp()
            #print(fingers)

            # Allow percentage value rather than just values, divided by 100 to make it from 0-10
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volPer/100, None)
                cv2.circle(img, (pointersInfo[4], pointersInfo[5]), 15, (0, 255, 0), cv2.FILLED)
            #    colorVol = (0, 255, 0)
            #else:
            #    colorVol = (255, 0, 0)

    # Drawings
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cVol = int(volume.GetMasterVolumeLevelScalar()*100)
    cv2.putText(img, f'Vol Set: {int(cVol)} %', (350, 50), cv2.FONT_HERSHEY_COMPLEX, 1, colorVol, 3)

    # Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)} %', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows() 