from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog, PhotoImage
import cv2

import detect
import read_results


class Main(object):
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='zobraz obrazek', command=self.open_image)
        self.pen_button.grid(row=0, column=0)

        self.brush_button = Button(self.root, text='kamera', command=self.open_video)
        self.brush_button.grid(row=1, column=0)

        self.color_button = Button(self.root, text='vyber plochu')
        self.color_button.grid(row=2, column=0)

        self.eraser_button = Button(self.root, text='eraser')
        self.eraser_button.grid(row=3, column=0)

        choices = ['zelene', 'cervene', 'oboje']
        variable = StringVar(self.root)
        variable.set('oboje')
        self.w = OptionMenu(self.root, variable, *choices)
        self.w.grid(row=4, column=0)

        self.label = Label(text="Hledany pocet ledek")
        self.label.grid(row=5, column=0)

        self.input = Entry(self.root)
        self.input.grid(row=6, column=0)

        self.start_button = Button(self.root, text='Spustit')
        self.start_button.grid(row=7, column=0)

        global my_text
        my_text = Text(height=20, width=30)
        my_text.grid(row=0, rowspan=3, column=2)

        self.stats_button = Button(self.root, text='Statistiky', command=self.open_text)
        self.stats_button.grid(row=7, column=2)

        self.save_button = Button(self.root, text='Uložit záznam', command=self.save_text)
        self.save_button.grid(row=8, column=2)

        self.c = Canvas(self.root, bg='white', width=590, height=780)
        self.c.grid(row=0, rowspan=10, column=1)

        self.root.mainloop()

    def open_image(self):
        global my_image
        self.filename = filedialog.askopenfilename(initialdir="C:/Users/a/Desktop/obrazky/", title="vyberte obrazek",
                                                   filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))

        my_image = Image.open(self.filename)
        my_image = my_image.resize((570, 760), Image.ANTIALIAS)
        my_image = ImageTk.PhotoImage(my_image)
        self.c.create_image(10, 10, image=my_image, anchor=NW)

    def open_video(self):
        global my_image
        self.filename = filedialog.askopenfilename(initialdir="C:/Users/a/Desktop/obrazky/", title="vyberte vydeo",
                                                   filetypes=(("mp4 files", "*.mp4"), ("all files", "*.*")))
        my_image = Image.open(self.filename)

    def open_text(self):

        text_file = filedialog.askopenfilename(initialdir="C:/Users/a/Desktop/obrazky/vysledky/",
                                              title="vyhledejte vysledky"
                                              , filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        text_file = open(text_file, 'r')
        stuff = text_file.read()

        my_text.insert(END, stuff)
        text_file.close()

    def save_text(self):
        text_file = filedialog.askopenfilename(initialdir="C:/Users/a/Desktop/obrazky/vysledky/",
                                              title="vyhledejte vysledky"
                                              , filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))






    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode


    def reset(self, event):
        self.old_x, self.old_y = None, None


if __name__ == '__main__':
    #Main()
    detect.picture_from_video()
    #detect.detection()



