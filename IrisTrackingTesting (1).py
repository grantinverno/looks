__author__ = 'Leandro Alberto-Dominguez'
#mhmm I tell ya hwhat now
import numpy as np
from matplotlib.pyplot import *
import cv2
import cv2.cv as cv
import time
import threading

cap = cv2.VideoCapture(0)
print "So far so good"

xvalues = []
yvalues = []



ycalib = [0, 90, 180, 270, 360, 450, 540, 630, 720]
xcalib = [0, 135, 270, 405, 540, 675, 810, 945, 1080]
fx = []
fy = []

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray,17)
    print "made it past the filtering"

    edges = cv2.Canny(blur, 10, 30)
    circles = cv2.HoughCircles(blur, cv.CV_HOUGH_GRADIENT, 1, 2000, param1=60, param2=30 , minRadius=70, maxRadius=130)

    print " made it past circle detection"
    if circles is  None:
        print "Did not find circles"

    else:
        circles = np.uint16(np.around(circles))
        for (x,y,r) in circles[0,:]:
            xvalues.append(x)
            yvalues.append(y)
            print "(" + str(x) + "," + str(y) + ")"
            cv2.circle(gray,(x,y), r, (255,255,0), 4)
            cv2.circle(gray,(x,y), 2, (255,255,0), 4)

    q = cv2.waitKey(25)
    if q == ord('q'):
        if len(fx) < 9:
            if circles is  None:
                print "Did not find circles"

            else:
                circles = np.uint16(np.around(circles))
                for (x,y,r) in circles[0, :]:
                    fx.append(x)
                    print "X CALIBRATION POINT NUMBER" + str(len(fx))
    w = cv2.waitKey(25)
    if w == ord('w'):
        if len(fy) < 9:
            if circles is  None:
                print "Did not find circles"

            else:
                circles = np.uint16(np.around(circles))
                for (x,y,r) in circles[0, :]:
                    fy.append(y)
                    print "Y CALIBRATION POINT NUMBER" + str(len(fy))

    if len(fy) == 9:
        fx = np.array(fx)
        fy = np.array(fy)

        xcalib = np.array(xcalib)
        ycalib = np.array(ycalib)

        xcoefficients = np.polyfit(xcalib, fx, 5)
        ycoefficients = np.polyfit(ycalib, fy, 5)

        xpolynomial = np.poly1d(xcoefficients)
        ypolynomial = np.poly1d(ycoefficients)

        xs = np.arange(0, 1080)
        ys = np.arange(0, 720)

        fxs = xpolynomial(xs)
        fys = ypolynomial(ys)


        yplot = figure()
        ax1 = yplot.add_subplot(111)
        ax1.plot(ys, fys)
        ax1.scatter(ycalib, fy)

        xplot = figure()
        ax2 = xplot.add_subplot(111)
        ax2.plot(xs, fxs)
        ax2.scatter(xcalib, fx)

        show()
        break
    cv2.imshow('Edges', edges)
    cv2.imshow('Circles', gray)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
         break

while True:
    print "Initialized Main Method"
    worldImg = np.zeros((720, 1080), np.uint8)
    ret, img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray,17)
    print "made it past the filtering"

    edges = cv2.Canny(blur, 10, 30)
    circles = cv2.HoughCircles(blur, cv.CV_HOUGH_GRADIENT, 1, 2000, param1=60, param2=30 , minRadius=0, maxRadius=200)

    print " made it past circle detection"
    if circles is  None:
        print "Did not find circles"

    else:
        circles = np.uint16(np.around(circles))
        for (x,y,r) in circles[0,:]:
            xview = int(xpolynomial(x))
            yview = int(ypolynomial(y))
            cv2.circle(gray,(x,y), r, (255,255,0), 4)
            cv2.circle(worldImg, (xview, yview), 100, (255, 255, 0), 4)

    cv2.imshow('WorldView', worldImg)
    #cv2.imshow('Edges', edges)
    cv2.imshow('Circles', gray)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break


cap.release()
cv2.destroyAllWindows()

