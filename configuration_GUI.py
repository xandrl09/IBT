#  Author: Ondřej Andlra
#


from tkinter import *
from tkinter import colorchooser, ttk
from PIL import ImageTk, Image
from tkinter import filedialog
import json




"""
Objekt Main je základní součástí alikace. 
"""


class Main(object):
    def __init__(self):
        self.root = Tk()

        # Proměnné pro výběr plochy
        self.x = self.y = 0  # koordinaty pro vyber plochy
        self.rectangle = None
        self.second_rectangle = None
        self.pocet_uloh = 1
        self.aktualni_uloha = self.pocet_uloh

        # JSON konfigurační soubor
        self.output_configuration_file = "C:/Users/a/Desktop/obrazky/konfigurace/konfigurace.json"  # todo zmenit
        data = {"uloha1": {}}

        with open(self.output_configuration_file, "w") as f:
            json.dump(data, f, indent=4)

        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha1"]
            temp["typ ulohy"] = "detekce LED"
            self.write_json(data)

        # Grid - ruzne velikosti
        Grid.rowconfigure(self.root, 9, weight=1)

        Grid.columnconfigure(self.root, 1, weight=3)
        Grid.columnconfigure(self.root, 2, weight=3)
        Grid.columnconfigure(self.root, 3, weight=3)
        Grid.columnconfigure(self.root, 4, weight=3)
        Grid.columnconfigure(self.root, 5, weight=3)
        Grid.columnconfigure(self.root, 6, weight=3)
        Grid.columnconfigure(self.root, 7, weight=3)
        Grid.columnconfigure(self.root, 8, weight=3)
        Grid.columnconfigure(self.root, 9, weight=1)
        Grid.columnconfigure(self.root, 10, weight=1)

        # Definice jednotlivích tlačítek
        # self.obr_frame = LabelFrame(self.root, text='nacteni obrazku')
        # self.obr_frame.grid(row=0, column=0)
        self.obr_button = Button(self.root, text='Zobraz nový obrázek', command=self.open_image)
        self.obr_button.grid(row=0, column=0)

        # self.camera_button = Button(self.root, text='kamera', command=self.open_video)
        # self.camera_button.grid(row=1, column=0)


        self.snip_frame = LabelFrame(self.root, text='Rychlost snímání', padx=5, pady=5)
        self.snip_frame.grid(row=0, column=1, rowspan=2)

        self.time_button = Button(self.snip_frame, text='potvrdit', command=self.scaning_speed)
        self.time_button.grid(row=1, column=1)

        self.time_input = Entry(self.snip_frame)
        self.time_input.grid(row=0, column=1)
        self.time_input.insert(END, '1000')

        self.choose_button = Button(self.root, text='vyber plochu', borderwidth=1, command=self.choose_area)
        self.choose_button.grid(row=1, column=2)


        self.color_picker = Button(self.root, text="vyber barvu", command=self.pick_color)
        self.color_picker.grid(row=0, column=2)

        self.led_frame = LabelFrame(self.root, text='Počet símaných LED', padx=5, pady=5)
        self.led_frame.grid(row=0, column=4, rowspan=2)

        self.input = Entry(self.led_frame)
        self.input.grid(row=0, column=4)
        self.input.insert(END, '64')

        self.led_number = Button(self.led_frame, text="zadat", command=self.led_number)
        self.led_number.grid(row=1, column=4)

        # Tlačítka pro definici a přepínání úloh
        self.new_work_button = Button(self.root, text="Nova uloha", command=self.new_work)
        self.new_work_button.grid(row=0, column=5)

        # self.actual_work_value = StringVar()
        # self.actual_work_value.set("Aktualni uloha je: uloha_" + str(self.aktualni_uloha))
        # self.actual_work = Label(self.root, text=self.actual_work_value.get())
        # self.actual_work.grid(row=1, column=5)

        self.choose_work_frame = LabelFrame(self.root, text='Výběr aktuální úlohy', padx=5, pady=5)
        self.choose_work_frame.grid(row=0, column=6)

        self.possibilities = 'uloha1'
        self.work_choose_combobox = ttk.Combobox(self.choose_work_frame, state='readonly')
        self.work_choose_combobox['values'] = self.possibilities
        self.work_choose_combobox.set("uloha1")
        self.work_choose_combobox.grid(row=0, column=6)
        self.work_choose_combobox.bind("<<ComboboxSelected>>", lambda _: self.change_work())

        # b = ttk.Button(self.root, text="Potvrdit vyber ulohy", command=self.change_work)
        # b.grid(row=1, column=6)

        # Zobrazování výsledků a konfigurace
        # self.start_button = Button(self.root, text='Spustit test', command=detect.picture_from_video)
        # self.start_button.grid(row=0, column=7)

        global my_text
        my_text = Text(height=30, width=40)
        my_text.grid(row=2, rowspan=6, column=8, columnspan=2)

        # automaticke vypsani konfigurace
        stuff = open(self.output_configuration_file).read()
        my_text.insert(END, stuff)

        self.stats_button = Button(self.root, text='Zobraz statistiky', command=self.open_text)
        self.stats_button.grid(row=0, column=8)

        self.stats_button = Button(self.root, text='Zobraz konfiguraci', command=self.open_config)
        self.stats_button.grid(row=0, column=9)

        self.c = Canvas(self.root, bg='white', width=980, height=560, cursor="cross")
        self.c.grid(row=2, columnspan=8, column=0)

        self.save_config_button = Button(self.root, text='Uložit konfiguraci', command=self.save_config)
        self.save_config_button.grid(row=1, column=9)

        # Zobrazení snímku
        global image
        global my_image

        image = Image.open("C:/Users/a/Desktop/obrazky/prezentace/44.jpg")  # todo zmenit
        image = image.resize((960, 540), Image.ANTIALIAS)

        my_image = ImageTk.PhotoImage(image)
        self.c.create_image(10, 10, image=my_image, anchor=NW)

        # try:
        #     self.start = Toplevel(self.root)
        #     self.start.attributes('-topmost', 'true')
        #     self.start.wm_title("Window")
        #     self.start.geometry("250x150")
        #
        #     self.obr_button = Button(self.start, text='Vyberte konfiguracni soubor', command=self.open_first_config)
        #     self.obr_button.grid(row=0, column=1)
        # except:
        #     pass

        self.root.mainloop()

    # funkce
    # def open_first_config(self):
    #     my_text.delete("1.0", "end")
    #     self.output_configuration_file = filedialog.asksaveasfilename(initialdir="C:/Users/a/Desktop/obrazky/konfigurace/",
    #                                            title="vyhledejte vysledky"
    #                                            , filetypes=(("JSON files", "*.json"), ("all files", "*.*")),
    #                                                                   command=self.start.destroy()
    #                                                                   )
    #
    #     data = {"uloha1": {}}
    #
    #     with open(self.output_configuration_file, "w") as f:
    #         json.dump(data, f, indent=4)
    #
    #     with open(self.output_configuration_file) as js:
    #         data = json.load(js)
    #         temp = data["uloha1"]
    #         temp["typ ulohy"] = "detekce LED"
    #         self.write_json(data)



    def open_image(self):
        global image
        global my_image
        self.filename = filedialog.askopenfilename(initialdir="/obrazky/prezentace/", title="vyberte obrazek",
                                                   filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))

        image = Image.open(self.filename)
        image = image.resize((960, 540), Image.ANTIALIAS)

        my_image = ImageTk.PhotoImage(image)
        self.c.create_image(10, 10, image=my_image, anchor=NW)

    # def open_video(self):
    #     pass
        # self.filename = filedialog.askopenfilename(initialdir="C:/Users/a/Desktop/obrazky/videa", title="vyberte vydeo",
        #                                            filetypes=(("mp4 files", "*.mp4"), ("all files", "*.*")))
        # text_file = open("C:/Users/a/Desktop/obrazky/konfigurace/config.txt", "w")
        # text_file.write(str(self.filename))

    def open_text(self):
        self.save_button = Button(self.root, text='Uložit záznam', command=self.save_text)
        self.save_button.grid(row=1, column=8)

        my_text.delete("1.0", "end")
        text_file = filedialog.askopenfilename(initialdir="/obrazky/vysledky/",
                                               title="vyhledejte vysledky"
                                               , filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        text_file = open(text_file, 'r')
        stuff = text_file.read()

        my_text.insert(END, stuff)
        text_file.close()

        self.save_config_button.grid_forget()

    def save_text(self):
        text_file = filedialog.askopenfilename(initialdir="/obrazky/vysledky/",
                                               title="vyhledejte vysledky"
                                               , filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))

    def open_config(self):
        my_text.delete("1.0", "end")
        text_file = filedialog.askopenfilename(initialdir="/obrazky/konfigurace/",
                                               title="vyhledejte vysledky"
                                               , filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        text_file = open(text_file, 'r')
        stuff = text_file.read()

        my_text.insert(END, stuff)
        text_file.close()

        self.save_config_button = Button(self.root, text='Uložit konfiguraci', command=self.save_config)
        self.save_config_button.grid(row=1, column=9)

        try:
            self.save_button.grid_forget()
        except:
            pass

    def save_config(self):
        text_file = filedialog.askopenfilename(initialdir="/Desktop/obrazky/konfigurace/",
                                               title="vyhledejte vysledky"
                                               , filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        self.output_configuration_file = text_file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))

    def scaning_speed(self):
        val = self.time_input.get()
        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha" + str(self.aktualni_uloha)]
            try:
                temp["rychlost snimani"] = val
                self.write_json(data)
            except:
                y = {"rychlost snimani": val}
                temp.append(y)
                self.write_json(data)

        self.update_configuration()


    def new_work(self):
        try:
            self.cancel_rectangle()
        except:
            pass
        self.pocet_uloh += 1
        self.aktualni_uloha = self.pocet_uloh
        # self.actual_work_value.set("Aktualni uloha je: uloha_" + str(self.aktualni_uloha))
        # self.actual_work = Label(self.root, text=self.actual_work_value.get())
        # self.actual_work.grid(row=1, column=5)

        self.possibilities += ' uloha' + str(self.aktualni_uloha)
        self.work_choose_combobox['values'] = self.possibilities
        self.work_choose_combobox.set(' uloha' + str(self.aktualni_uloha))

        self.work_type()
        try:
            self.color_label.grid_forget()
            self.color_tolerance_picker.grid_forget()
        except:
            pass

        with open(self.output_configuration_file) as js:
            data = json.load(js)
            y = {"uloha" + str(self.pocet_uloh): {}}
            data.update(y)
            self.write_json(data)

    def work_type(self):
        self.win = Toplevel(self.root)
        self.win.wm_title("Window")
        self.win.geometry("250x150")

        l = Label(self.win, text="Vyberte typ ulohy")
        l.grid(row=0, column=0)

        possibilities = ('Detekce LED', 'Mereni vzdalenosti')
        self.work_combo = ttk.Combobox(self.win, state='readonly')
        self.work_combo['values'] = possibilities
        self.work_combo.set("Detekce LED")


        self.work_combo.grid(row=1, column=0)

        b = ttk.Button(self.win, text="Potvrdit", command=self.change_type)
        b.grid(row=2, column=0)

    def change_type(self):
        var = self.work_combo.get()
        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha" + str(self.pocet_uloh)]
            try:
                temp["typ ulohy"] = var
                self.write_json(data)
            except:
                y = {"typ ulohy": var}
                temp.append(y)
                self.write_json(data)

        self.update_configuration()
        self.win.destroy()

    def change_work(self):
        try:
            self.cancel_rectangle()
        except:
            pass
        var = self.work_choose_combobox.get()
        s = None
        for s in var.split("a"):
            if s.isdigit():
                int(s)
        self.aktualni_uloha = s
        self.work_choose_combobox.set("uloha" + str(s))

        try:
            with open(self.output_configuration_file) as js:
                data = json.load(js)
                temp = data["uloha" + str(self.aktualni_uloha)]
                x0, y0 = temp["pozice"][0], temp["pozice"][1]
                x1, y1 = temp["pozice"][2], temp["pozice"][3]
                self.rectangle = self.c.create_rectangle(x0, y0, x1, y1, outline='#00d0e8', width=2)
                self.second_rectangle = self.c.create_rectangle(x0 - 2, y0 - 2, x1 + 2, y1 + 2, outline='yellow',
                                                                width=2)
        except:
            pass

    def choose_area(self):
        try:
            self.cancel_rectangle()
        except:
            pass
        self.c.bind("<ButtonPress-1>", self.on_button_press)
        self.c.bind("<ButtonRelease-1>", self.on_button_release)

    def cancel_rectangle(self):
        self.c.delete(self.rectangle)
        self.c.delete(self.second_rectangle)

    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y

    def on_button_release(self, event):
        x0, y0 = (self.x, self.y)
        x1, y1 = (event.x, event.y)
        self.rectangle = self.c.create_rectangle(x0, y0, x1, y1, outline='#00d0e8', width=2)
        self.second_rectangle = self.c.create_rectangle(x0 - 2, y0 - 2, x1 + 2, y1 + 2, outline='yellow', width=2)

        self.c.unbind("<ButtonPress-1>")
        self.c.unbind("<ButtonRelease-1>")

        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha" + str(self.aktualni_uloha)]
            try:
                temp["pozice"] = [x0, y0, x1, y1]
                self.write_json(data)
            except:
                y = {"pozice": [x0, y0, x1, y1]}
                temp.append(y)
                self.write_json(data)

        self.update_configuration()

    def pick_color(self):
        self.c.bind("<ButtonPress-1>", self.button_press)

    def button_press(self, event):
        global image
        global barva
        self.x = event.x
        self.y = event.y
        x0, y0 = (self.x, self.y)
        barva = image.getpixel((x0, y0))
        self.c.unbind("<ButtonPress-1>")
        self.color()

    def color(self):
        global barva
        my_color = colorchooser.askcolor(barva)[1]

        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha" + str(self.aktualni_uloha)]
            try:
                temp["barva"] = my_color
                self.write_json(data)
            except:
                y = {"barva": my_color}
                temp.append(y)
                self.write_json(data)

        self.update_configuration()

        self.color_label = LabelFrame(self.root, text="Nastavit tolaranci barvi")
        self.color_label.grid(row=0, column=3)
        self.color_tolerance_picker = Scale(self.color_label, from_=0, to=150, orient=HORIZONTAL, command=self.pick_tolerance)
        self.color_tolerance_picker.set(75)
        self.color_tolerance_picker.grid(row=0, column=3)

    def pick_tolerance(self, val):
        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha" + str(self.aktualni_uloha)]
            try:
                temp["tolerance"] = val
                self.write_json(data)
            except:
                y = {"tolerance": val}
                temp.append(y)
                self.write_json(data)

        self.update_configuration()

    def led_number(self):
        val = self.input.get()
        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha" + str(self.aktualni_uloha)]
            try:
                temp["pocet LED"] = val
                self.write_json(data)
            except:
                y = {"pocet LED": val}
                temp.append(y)
                self.write_json(data)

        self.update_configuration()

    def write_json(self, data):
        with open(self.output_configuration_file, "w") as o:
            json.dump(data, o, indent=4)

    def update_configuration(self):
        my_text.delete("1.0", "end")
        text_file = open(self.output_configuration_file, 'r')
        stuff = text_file.read()

        my_text.insert(END, stuff)
        text_file.close()


if __name__ == '__main__':
    Main()
