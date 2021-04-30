import cv2
import numpy as np
import time
import os
from datetime import datetime
import json
from PIL import ImageColor

import sys
import getopt

counter = 0
is_new_product = True
is_second_product = False
input_camera = None
input_configuration_file = None
output_configuration_file = None
output_configuration_file_address = None


def parse_params():
    global input_camera
    global input_configuration_file
    global output_configuration_file_address

    arguments = sys.argv[1:]
    options = "a:i:o:"
    try:
        opts, args = getopt.getopt(arguments, options)
    except getopt.GetoptError as err:
        print(err)
        opts = []

    for opt, arg in opts:
        if opt in ['-a']:
            input_camera = arg
        elif opt in ['-i']:
            input_configuration_file = arg
        elif opt in ['-o']:
            output_configuration_file_address = arg


def write_json(data):
    global output_configuration_file
    with open(output_configuration_file, "w") as o:
        json.dump(data, o, indent=4)


# Funkce načte z konfiguračního souboru odkaz na kameru a získává z ní
# snímky jednotlivích výrobků.
def picture_from_video():
    global input_configuration_file
    global output_configuration_file
    global output_configuration_file_address
    global input_camera
    #captured_video = cv2.VideoCapture("C:/Users/a/Desktop/obrazky/videa/b.mp4")
    #configuration_file = open("C:/Users/a/Desktop/obrazky/konfigurace/config.txt", "r")
    captured_video = cv2.VideoCapture(input_camera)
    fps = int(captured_video.get(cv2.CAP_PROP_FPS))
    j = 0
    stri = str(datetime.today().strftime('%Y_%m_%d_%H_%M_%S'))
    output_configuration_file = output_configuration_file_address + stri + ".json"  # todo zmenit

    # JSON
    data = {}
    with open(output_configuration_file, "w") as f:
        json.dump(data, f, indent=4)

    #output_configuration_file.close()

    while True:
        j += 1
        for i in range(fps - 1):
            captured_video.read()
        ret, img = captured_video.read()

        try:
            #cv2.imwrite("C:/Users/a/Desktop/obrazky/test/" + str(j + 40) + ".jpg", img)
            with open(input_configuration_file) as js:
                input_data = json.load(js)
                for a in input_data:
                    #print(a)
                    cimg = detection(img, a, j)
        except:
            break
        cv2.imwrite("C:/Users/a/Desktop/obrazky/test/" + str(j + 20) + ".jpg", cimg)




def detection(img, a, j):
    global counter
    global is_new_product
    global is_second_product
    global input_configuration_file
    global output_configuration_file

    # video resize 1920 1080 -> 960 540
    img = cv2.resize(img, (960, 540))

    with open(input_configuration_file) as js:
        input_data = json.load(js)
        input_temp = input_data[a]
        try:
            ledky = input_temp["pocet LED"]
        except:
            ledky = 64
        try:
            x, xx = input_temp["pozice"][0], input_temp["pozice"][2]
            x -= 10
            xx -= 10
            y, yy = input_temp["pozice"][1], input_temp["pozice"][3]
            y -= 10
            yy -= 10
            img = img[y:yy, x:xx]  #
        except:
            pass
        try:
            color = input_temp["barva"]
            dispersion = input_temp["tolerance"]
            R, G, B = ImageColor.getcolor(color, "RGB")
            print(R, G, B)
            lower_range = np.array([R - int(dispersion), G - int(dispersion), B - int(dispersion)])
            upper_range = np.array([R + int(dispersion * 3), G + int(dispersion), B + int(dispersion)])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            mask = cv2.inRange(img, lower_range, upper_range )
            #cv2.imwrite("C:/Users/a/Desktop/obrazky/test/" + str(j) + ".jpg", mask)
            colored_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            rows = colored_img.shape[0]
            circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 28, param1=90, param2=13, minRadius=15,
                                       maxRadius=30)
        except:
            lower_range = np.array([0, 174, 0]) #  todo
            upper_range = np.array([255, 255, 93])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            mask = cv2.inRange(img, lower_range, upper_range)
            #cv2.imwrite("C:/Users/a/Desktop/obrazky/test/" + str(j) + ".jpg", mask)
            colored_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            rows = colored_img.shape[0]
            circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 28, param1=90, param2=13, minRadius=15,
                                       maxRadius=30)
            # # cv2.imwrite("C:/Users/a/Desktop/obrazky/test/" + str(j) + ".jpg", img)
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # prevod do sedotonu
            # #cv2.imwrite("C:/Users/a/Desktop/obrazky/test/" + str(j) + ".jpg", img)
            # img = cv2.medianBlur(img, 1)
            # treshold, tresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
            # cv2.imwrite("C:/Users/a/Desktop/obrazky/test/" + str(j) + ".jpg", tresh)
            # colored_img = cv2.cvtColor(tresh, cv2.COLOR_GRAY2BGR)
            # rows = colored_img.shape[0]
            # circles = cv2.HoughCircles(tresh, cv2.HOUGH_GRADIENT, 1, 28, param1=90, param2=13, minRadius=15,
            #                            maxRadius=30)

    # led detection
    if circles is not None:
        if is_new_product == True:
            if is_second_product == False:
                is_second_product = True
            else:
                counter += 1
                with open(output_configuration_file) as js:
                    data = json.load(js)
                    o = {"vyrobek" + str(counter): {}}
                    data.update(o)
                    write_json(data)

                with open(output_configuration_file) as js:
                    data = json.load(js)
                    temp = data["vyrobek" + str(counter)]
                    i = {str(a): {}}
                    temp.update(i)
                    write_json(data)

                pocet_ledek = len(circles[0, :])

                if pocet_ledek == int(ledky):
                    with open(output_configuration_file) as js:
                        data = json.load(js)
                        temp = data["vyrobek" + str(counter)]
                        t = temp[str(a)]
                        y = {"stav": "vporadku"}
                        t.update(y)
                        write_json(data)
                else:
                    with open(output_configuration_file) as js:
                        data = json.load(js)
                        temp = data["vyrobek" + str(counter)]
                        t = temp[str(a)]
                        y = {"stav": "vadny"}
                        print(int(ledky) - pocet_ledek)
                        y["chyby"] = int(ledky) - pocet_ledek
                        t.update(y)
                        write_json(data)

                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    # draw the outer circle
                    cv2.circle(colored_img, (i[0], i[1]), i[2], (0, 0, 255), 2)
                    # draw the center of the circle
                    # cv2.circle(colored_img, (i[0], i[1]), 1, (0, 0, 255), 2)
                is_new_product = False
                is_second_product = False
    else:
        is_second_product = False
        if is_new_product == False:
            is_new_product = True

    return colored_img


# def color_detection()


# Funkce zobrazý snímek obsahující detekované objekty.
def show_detected(cimg):
    cv2.namedWindow('detected circles', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('detected circles', 570, 760)

    cv2.imshow('detected circles', cimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Funkce zobrazý snímek vzniklí prahováním.
def show_threshold(tresh):
    cv2.namedWindow('threshold', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('threshold', 570, 760)
    cv2.imshow('threshold', tresh)


#
def all_circle_detection(img, cimg):
    circles1 = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 28,
                                param1=100, param2=30, minRadius=30, maxRadius=60)

    if circles1 is not None:
        circles1 = np.uint16(np.around(circles1))
        for i in circles1[0, :]:
            # draw the outer circle
            cv2.circle(cimg, (i[0], i[1]), i[2], (0, 255, 0), 2)


def main():
    parse_params()
    picture_from_video()


if __name__ == '__main__':
    main()
