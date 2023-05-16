import cv2
import numpy as np
import autopy
import HandDetector as htm
import time
import mediapipe as mp

wCam, hCam = 640, 480
cTime = 0
pTime = 0
height = 480
width= 640
smoothening = 8
plocX, plocY = 0, 0
clocX, clocY = 0, 0
frameR = 100
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0
cap = cv2.VideoCapture(0)
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector= htm.handDetector(maxHands=2)
screen_width, screen_height = autopy.screen.size()
#wScr, hScr = autopy.screen.size()
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist, bbox = detector.findPosition(img)
    #2
    #if len(lmList) != 0:
     #   x1, y1 = lmList[8][1:]
      #  x2, y2 = lmList[12][1:]

    #fingers = detector.fingersUp()
    #print(fingers)
    #cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
    #(255, 0, 255), 2)
    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255),
                      2)
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, width - frameR), (0, screen_width))
            y3 = np.interp(y1, (frameR, height - frameR), (0, screen_height))

            curr_x = prev_x + (x3 - prev_x) / smoothening
            curr_y = prev_y + (y3 - prev_y) / smoothening

            autopy.mouse.move(screen_width - curr_x, curr_y)
            cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y

        if fingers[1] == 1 and fingers[2] == 1:
            length, img, lineInfo = detector.findDistance(8, 12, img)

            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()
    #11

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    #12
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break