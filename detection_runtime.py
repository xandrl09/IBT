#########################################
#  Skript pro detekci kruhových objektů #
#                                       #
#  Author: Ondřej Andlra                #
#  Email: xandrl09@stud.fit.vutbr.cz    #
#  Rok: 2021                            #
#########################################

# importovani potrebnych knihoven
import cv2
import numpy as np
from datetime import datetime
import json
from PIL import ImageColor
import sys
import getopt

# definice globálních proměnných
counter = 0
is_new_product = True
is_second_product = False
input_camera = None
input_configuration_file = None
output_configuration_file = None
output_configuration_file_address = None


# funkce pro zpracování parametrů
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
        if opt in ['-a']:  # adresa videa
            input_camera = arg
        elif opt in ['-i']:  # adresa konfiguracniho souboru
            input_configuration_file = arg
        elif opt in ['-o']:  # adresa slozky pro soubor s vysledky
            output_configuration_file_address = arg


# funkce pro zapis vysledku ve formatu JSON
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
    rychlost = 1

    captured_video = cv2.VideoCapture(input_camera)
    fps = int(captured_video.get(cv2.CAP_PROP_FPS))

    # soubor s vysledky pojmenovan podle data provedeni detekce
    stri = str(datetime.today().strftime('%Y_%m_%d_%H_%M_%S'))
    # soubor s vysledky
    output_configuration_file = output_configuration_file_address + stri + ".json"

    # JSON
    data = {}
    with open(output_configuration_file, "w") as f:
        json.dump(data, f, indent=4)

    try:
        with open(input_configuration_file) as js:
            input_data = json.load(js)
            input_temp = input_data[0]
            #
            rychlost = input_temp["rychlost snimani"]
            if rychlost < 500:
                rychlost = 500
            if rychlost > 2000:
                rychlost = 2000
            rychlost = int(rychlost / 1000)

    except:
            pass

    while True:
        for i in range(fps * rychlost - 1):
            captured_video.read()
        ret, img = captured_video.read()

        try:
            with open(input_configuration_file) as js:
                input_data = json.load(js)
                for a in input_data:
                    color_img = detection(img, a)
        except:
            break


# funkce provadi detekci kruhovych objektu v obraze
def detection(img, a):
    global counter
    global is_new_product
    global is_second_product
    global input_configuration_file
    global output_configuration_file

    green_lower_range = 174
    blue_upper_range = 93

    # video resize 1920 1080 -> 960 540
    img = cv2.resize(img, (960, 540))

    with open(input_configuration_file) as js:
        input_data = json.load(js)
        input_temp = input_data[a]
        # pokud je v konfiguraci specifikovan pocet LED
        try:
            ledky = input_temp["pocet LED"]
        except:
            ledky = 64
        # pokud je v konfiguraci specifikovana pozice obdelniku pro hledani
        # odecitani -10 = korekce toho, ze GUI pripocitava v Canvas 10 na okraj
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
        # pokud je v konfiguraci specifikovana barva
        try:
            color = input_temp["barva"]
            dispersion = input_temp["tolerance"]
            R, G, B = ImageColor.getcolor(color, "RGB")
            lower_range = np.array([R - int(dispersion), G - int(dispersion), B - int(dispersion)])
            upper_range = np.array([R + int(dispersion * 3), G + int(dispersion), B + int(dispersion)])
        # pokud neni barva specifikovana
        except:
            lower_range = np.array([0, green_lower_range, 0])
            upper_range = np.array([255, 255, blue_upper_range])

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mask = cv2.inRange(img, lower_range, upper_range)
        colored_img = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        rows = colored_img.shape[0]
        detected_circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 28, param1=90, param2=13, minRadius=15,
                                            maxRadius=30)

    #  detekce LED
    if detected_circles is not None:
        if is_new_product == True:
            if is_second_product == False: # vyfiltrování prvních přesvětlených snímků
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

                pocet_ledek = len(detected_circles[0, :])

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
                        # print(int(ledky) - pocet_ledek)
                        y["chyby"] = int(ledky) - pocet_ledek
                        t.update(y)
                        write_json(data)

                detected_circles = np.uint16(np.around(detected_circles))
                for i in detected_circles[0, :]:
                    # vykresleni detekovaných kružnic
                    cv2.circle(colored_img, (i[0], i[1]), i[2], (0, 0, 255), 2)

                is_new_product = False
                is_second_product = False
    else:
        is_second_product = False
        if is_new_product == False:
            is_new_product = True

    return colored_img


# hlavni funkce
# volá zpracovani paramerů a detekci objektů
def main():
    parse_params()
    picture_from_video()


if __name__ == '__main__':
    main()
