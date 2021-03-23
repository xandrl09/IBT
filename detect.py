import cv2
import numpy as np
import time
import os
from datetime import datetime


from PIL import Image

import results
import main


counter = 0
novy = True


def picture_from_video():

    #cap = cv2.VideoCapture("C:/Users/a/Desktop/obrazky/videa/b.mp4")
    config = open("C:/Users/a/Desktop/obrazky/konfigurace/config.txt", "r")
    cap = cv2.VideoCapture(config.readline())
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    j = 0
    stri = str(datetime.today().strftime('%Y_%m_%d_%H_%M_%S'))
    filename = "C:/Users/a/Desktop/obrazky/vysledky/" + stri + ".txt"
    text_file = open(filename, "x")#
    text_file.write("Test probehl v :" + str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S')) + " \n")
    text_file.close()
    text_file = open(filename, 'a')
    while True:
        j += 1
        for i in range(fps - 1):
            cap.read()
        ret, img = cap.read()
        #if j == 5:
         #   break
        try:
            cimg = detection(img, text_file, j)
        except:
            text_file.close()
            break
        cv2.imwrite("C:/Users/a/Desktop/obrazky/test/" + str(j) + ".jpg", cimg)




"""
def crop_image():
    img2 = img.crop([left, upper, right, lower])
    return
"""


def detection(img, text_file, j):
    global counter
    global novy
    ledky = 64
    #cv2.imwrite("C:/Users/a/Desktop/obrazky/test/" + str(j) + ".jpg", img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # prevod do sedotonu
    #img = cv2.imread("C:/Users/a/Desktop/obrazky/3lines/big_0.jpg", 0)
    # picture resize 3016 4032 -> 570 760 video resize 1920 1080 -> 960 540
    img = cv2.resize(img, (960, 540))

    img = cv2.medianBlur(img, 1)
    treshold, tresh = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    # show_threshold(tresh);
    #cv2.imwrite("C:/Users/a/Desktop/obrazky/test/" + str(j) + str(j) + ".jpg", tresh)
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    rows = cimg.shape[0]

    # led detection
    circles = cv2.HoughCircles(tresh, cv2.HOUGH_GRADIENT, 1, 28, param1=110, param2=13, minRadius=15, maxRadius=30)

    if circles is not None:
        if novy == True:
            counter += 1
            text_file.write("Vyrobek " + str(counter))
            pocet_ledek = len(circles[0,:])
            if pocet_ledek == ledky:
                text_file.write(" je v poradku, ma:" + str(pocet_ledek) + " funkcnich ledek\n")
            else:
                text_file.write(" je vadny, ma: " + str(pocet_ledek) + "funkcnich ledek a " + str(ledky - pocet_ledek)
                                + " nefunkcnich\n")
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                # draw the outer circle
                cv2.circle(cimg, (i[0], i[1]), i[2], (0, 0, 255), 2)
                # draw the center of the circle
                # cv2.circle(cimg, (i[0], i[1]), 1, (0, 0, 255), 2)
            novy = False
    else:
        if novy == False:
            novy = True

    #show_detected(cimg)
    return cimg


def show_detected(cimg):
    cv2.namedWindow('detected circles', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('detected circles', 570, 760)

    cv2.imshow('detected circles', cimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_threshold(tresh):
    cv2.namedWindow('threshold', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('threshold', 570, 760)
    cv2.imshow('threshold', tresh)


def all_circle_detection(img, cimg):
    circles1 = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 28,
                                param1=100, param2=30, minRadius=30, maxRadius=60)

    if circles1 is not None:
        circles1 = np.uint16(np.around(circles1))
        for i in circles1[0, :]:
            # draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)




