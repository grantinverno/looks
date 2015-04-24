__author__ = 'Leandro Alberto-Dominguez'
#mhmm I tell ya hwhat now

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(1):
    ret, frame = cap.read()

    blur = cv2.medianBlur(frame,5)


    cv2.imshow('adaptiveThreshold',blur)
    cv2.imshow('original', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()