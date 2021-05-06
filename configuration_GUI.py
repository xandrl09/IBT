######################################
#  Konfigurační GUI aplikace         #
#                                    #
#  Autor: Ondřej Andlra             #
#  Email: xandrl09@stud.fit.vutbr.cz #
#  Rok: 2021                         #
######################################

# importovani potrebnych knhoven
from tkinter import *
from tkinter import colorchooser, ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import json


#  Objekt Main je základní součástí alikace.
class Main(object):
    def __init__(self):
        self.root = Tk()

        # Proměnné pro výběr plochy
        self.x = self.y = 0  # koordinaty pro vyber plochy
        self.first_rectangle = None
        self.second_rectangle = None
        self.work_counter = 1
        self.actual_work = self.work_counter

        # JSON konfigurační soubor
        self.output_configuration_file = "konfigurace/konfigurace.json"
        json_data = {"uloha1": {}}

        with open(self.output_configuration_file, "w") as f:
            json.dump(json_data, f, indent=4)

        with open(self.output_configuration_file) as js:
            json_data = json.load(js)
            json_temp = json_data["uloha1"]
            json_temp["typ ulohy"] = "detekce LED"
            self.write_json(json_data)

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
        self.obr_button = Button(self.root, text='Zobraz nový obrázek', command=self.open_image)
        self.obr_button.grid(row=0, column=0)

        # Tlacitka pro rychlost snimani
        self.snip_frame = LabelFrame(self.root, text='Rychlost snímání', padx=5, pady=5)
        self.snip_frame.grid(row=0, column=1, rowspan=2)

        self.time_button = Button(self.snip_frame, text='potvrdit', command=self.scaning_speed)
        self.time_button.grid(row=1, column=1)

        self.time_input = Entry(self.snip_frame)
        self.time_input.grid(row=0, column=1)
        self.time_input.insert(END, '1000')

        # Tlacitko pro vyber plochy
        self.choose_area_button = Button(self.root, text='vyber plochu', borderwidth=1, command=self.choose_area)
        self.choose_area_button.grid(row=1, column=2)

        # Tlacitko pro vyber barvy
        self.color_picker = Button(self.root, text="vyber barvu", command=self.pick_color)
        self.color_picker.grid(row=0, column=2)

        # Tlacitka pro vyber poctu LED
        self.led_frame = LabelFrame(self.root, text='Počet símaných LED', padx=5, pady=5)
        self.led_frame.grid(row=0, column=4, rowspan=2)

        self.led_input = Entry(self.led_frame)
        self.led_input.grid(row=0, column=4)
        self.led_input.insert(END, '64')

        self.led_number = Button(self.led_frame, text="zadat", command=self.led_number)
        self.led_number.grid(row=1, column=4)

        # Tlačítka pro definici a přepínání úloh
        self.new_work_button = Button(self.root, text="Nova uloha", command=self.new_work)
        self.new_work_button.grid(row=0, column=5)

        self.choose_work_frame = LabelFrame(self.root, text='Výběr aktuální úlohy', padx=5, pady=5)
        self.choose_work_frame.grid(row=0, column=6)

        self.work_possibilities = 'uloha1'
        self.work_choose_combobox = ttk.Combobox(self.choose_work_frame, state='readonly')
        self.work_choose_combobox['values'] = self.work_possibilities
        self.work_choose_combobox.set("uloha1")
        self.work_choose_combobox.grid(row=0, column=6)
        self.work_choose_combobox.bind("<<ComboboxSelected>>", lambda _: self.change_work())

        # Zobrazování výsledků a konfigurace
        global shown_text
        shown_text = Text(height=30, width=40)
        shown_text.grid(row=2, rowspan=6, column=8, columnspan=2)

        # automaticke vypsani konfigurace
        json_to_print = open(self.output_configuration_file).read()
        shown_text.insert(END, json_to_print)

        # tlacitka pro vypsani konfigurace a statistik
        self.stats_button = Button(self.root, text='Zobraz statistiky', command=self.open_text)
        self.stats_button.grid(row=0, column=8)

        self.config_button = Button(self.root, text='Zobraz konfiguraci', command=self.open_config)
        self.config_button.grid(row=0, column=9)

        self.plocha = Canvas(self.root, bg='white', width=980, height=560, cursor="cross")
        self.plocha.grid(row=2, columnspan=8, column=0)

        self.save_config_button = Button(self.root, text='Uložit konfiguraci', command=self.save_config)
        self.save_config_button.grid(row=1, column=9)

        # Zobrazení snímku
        global loaded_image
        global procesed_image

        loaded_image = Image.open("prezentace/44.jpg")  
        loaded_image = loaded_image.resize((960, 540), Image.ANTIALIAS)

        procesed_image = ImageTk.PhotoImage(loaded_image)
        self.plocha.create_image(10, 10, image=procesed_image, anchor=NW)

        # zpusteni hlavni smycky
        self.root.mainloop()

    #############################################################################
    # definice funkcí
    #############################################################################

    # nacteni obrazku
    def open_image(self):
        global loaded_image
        global procesed_image
        self.filename = filedialog.askopenfilename(initialdir="prezentace/", title="vyberte obrazek",
                                                   filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))

        loaded_image = Image.open(self.filename)
        loaded_image = loaded_image.resize((960, 540), Image.ANTIALIAS)

        procesed_image = ImageTk.PhotoImage(loaded_image)
        self.plocha.create_image(10, 10, image=procesed_image, anchor=NW)

    # nacteni vysledku
    def open_text(self):
        self.save_button = Button(self.root, text='Uložit záznam', command=self.save_text)
        self.save_button.grid(row=1, column=8)

        shown_text.delete("1.0", "end")
        text_file = filedialog.askopenfilename(initialdir="/obrazky/vysledky/",
                                               title="vyhledejte vysledky"
                                               , filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        text_file = open(text_file, 'r')
        stuff = text_file.read()

        shown_text.insert(END, stuff)
        text_file.close()

        self.save_config_button.grid_forget()

    # ulozeni vysledku
    def save_text(self):
        text_file = filedialog.askopenfilename(initialdir="/obrazky/vysledky/",
                                               title="vyhledejte vysledky"
                                               , filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        text_file = open(text_file, 'w')
        text_file.write(shown_text.get(1.0, END))

    # nacteni konfiguracniho souboru
    def open_config(self):
        shown_text.delete("1.0", "end")
        text_file = filedialog.askopenfilename(initialdir="/obrazky/konfigurace/",
                                               title="vyhledejte vysledky"
                                               , filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        text_file = open(text_file, 'r')
        stuff = text_file.read()

        shown_text.insert(END, stuff)
        text_file.close()

        self.save_config_button = Button(self.root, text='Uložit konfiguraci', command=self.save_config)
        self.save_config_button.grid(row=1, column=9)

        try:
            self.save_button.grid_forget()
        except:
            pass

    # ulozeni konfiguracniho souboru
    def save_config(self):
        text_file = filedialog.askopenfilename(initialdir="/Desktop/obrazky/konfigurace/",
                                               title="vyhledejte vysledky"
                                               , filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        self.output_configuration_file = text_file
        text_file = open(text_file, 'w')
        text_file.write(shown_text.get(1.0, END))

    # vyber rychlosti snimani snimku z videa
    def scaning_speed(self):
        val = self.time_input.get()
        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha" + str(self.actual_work)]
            try:
                temp["rychlost snimani"] = val
                self.write_json(data)
            except:
                y = {"rychlost snimani": val}
                temp.append(y)
                self.write_json(data)

        self.update_configuration()

    # vytvoreni nove ulohy
    def new_work(self):
        try:
            self.cancel_rectangle()
        except:
            pass
        self.work_counter += 1
        self.actual_work = self.work_counter

        self.work_possibilities += ' uloha' + str(self.actual_work)
        self.work_choose_combobox['values'] = self.work_possibilities
        self.work_choose_combobox.set(' uloha' + str(self.actual_work))

        self.work_type()
        try:
            self.color_label.grid_forget()
            self.color_tolerance_picker.grid_forget()
        except:
            pass

        with open(self.output_configuration_file) as js:
            data = json.load(js)
            y = {"uloha" + str(self.work_counter): {}}
            data.update(y)
            self.write_json(data)

    # vyber typu nove ulohy
    def work_type(self):
        self.win = Toplevel(self.root)
        self.win.wm_title("Window")
        self.win.geometry("250x150")

        new_work_type_label = Label(self.win, text="Vyberte typ ulohy")
        new_work_type_label.grid(row=0, column=0)

        possibilities = ('Detekce LED', 'Mereni vzdalenosti')
        self.work_combo = ttk.Combobox(self.win, state='readonly')
        self.work_combo['values'] = possibilities
        self.work_combo.set("Detekce LED")

        self.work_combo.grid(row=1, column=0)

        b = ttk.Button(self.win, text="Potvrdit", command=self.change_type)
        b.grid(row=2, column=0)

    # zmena typu ulohy
    def change_type(self):
        var = self.work_combo.get()
        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha" + str(self.work_counter)]
            try:
                temp["typ ulohy"] = var
                self.write_json(data)
            except:
                y = {"typ ulohy": var}
                temp.append(y)
                self.write_json(data)

        self.update_configuration()
        self.win.destroy()

    # zmena aktualni ulohy
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
        self.actual_work = s
        self.work_choose_combobox.set("uloha" + str(s))

        try:
            with open(self.output_configuration_file) as js:
                data = json.load(js)
                temp = data["uloha" + str(self.actual_work)]
                x0, y0 = temp["pozice"][0], temp["pozice"][1]
                x1, y1 = temp["pozice"][2], temp["pozice"][3]
                self.first_rectangle = self.plocha.create_rectangle(x0, y0, x1, y1, outline='#00d0e8', width=2)
                self.second_rectangle = self.plocha.create_rectangle(x0 - 2, y0 - 2, x1 + 2, y1 + 2, outline='yellow',
                                                                     width=2)
        except:
            pass

    # vyber plochy pro detekci
    def choose_area(self):
        try:
            self.cancel_rectangle()
        except:
            pass
        self.plocha.bind("<ButtonPress-1>", self.on_button_press)
        self.plocha.bind("<ButtonRelease-1>", self.on_button_release)

    # zruseni obdelniku pro vyber ulohy
    def cancel_rectangle(self):
        self.plocha.delete(self.first_rectangle)
        self.plocha.delete(self.second_rectangle)

    # ziskani polohy po kliknutí myší při víběru plochy pro detekci
    def on_button_press(self, event):
        self.x = event.x
        self.y = event.y

    # akce po puštění miši při víběru plochy pro detekci
    def on_button_release(self, event):
        x0, y0 = (self.x, self.y)
        x1, y1 = (event.x, event.y)
        self.first_rectangle = self.plocha.create_rectangle(x0, y0, x1, y1, outline='#00d0e8', width=2)
        self.second_rectangle = self.plocha.create_rectangle(x0 - 2, y0 - 2, x1 + 2, y1 + 2, outline='yellow', width=2)

        self.plocha.unbind("<ButtonPress-1>")
        self.plocha.unbind("<ButtonRelease-1>")

        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha" + str(self.actual_work)]
            try:
                temp["pozice"] = [x0, y0, x1, y1]
                self.write_json(data)
            except:
                y = {"pozice": [x0, y0, x1, y1]}
                temp.append(y)
                self.write_json(data)

        self.update_configuration()

    # funkce pro vyber barvy z obrazu
    def pick_color(self):
        self.plocha.bind("<ButtonPress-1>", self.button_press)

    # akce po kliknuti do snimku pri vyberu barvy
    def button_press(self, event):
        global loaded_image
        global barva
        self.x = event.x
        self.y = event.y
        x0, y0 = (self.x, self.y)
        barva = loaded_image.getpixel((x0, y0))
        self.plocha.unbind("<ButtonPress-1>")
        self.color()

    # ulozeni vybrane barvy
    def color(self):
        global barva
        my_color = colorchooser.askcolor(barva)[1]

        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha" + str(self.actual_work)]
            try:
                temp["barva"] = my_color
                self.write_json(data)
            except:
                y = {"barva": my_color}
                temp.append(y)
                self.write_json(data)

        self.update_configuration()

        # vytvoreni tlacitka pro vyber tolerance barvy
        self.color_label = LabelFrame(self.root, text="Nastavit tolaranci barvi")
        self.color_label.grid(row=0, column=3)
        self.color_tolerance_picker = Scale(self.color_label, from_=0, to=150, orient=HORIZONTAL, command=self.pick_tolerance)
        self.color_tolerance_picker.set(75)
        self.color_tolerance_picker.grid(row=0, column=3)

    # výběr tolerance barvy
    def pick_tolerance(self, val):
        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha" + str(self.actual_work)]
            try:
                temp["tolerance"] = val
                self.write_json(data)
            except:
                y = {"tolerance": val}
                temp.append(y)
                self.write_json(data)

        self.update_configuration()

    # výběr počtu LED
    def led_number(self):
        val = self.led_input.get()
        with open(self.output_configuration_file) as js:
            data = json.load(js)
            temp = data["uloha" + str(self.actual_work)]
            try:
                temp["pocet LED"] = val
                self.write_json(data)
            except:
                y = {"pocet LED": val}
                temp.append(y)
                self.write_json(data)

        self.update_configuration()

    # zapis dat do koniguracniho souboru
    def write_json(self, data):
        with open(self.output_configuration_file, "w") as o:
            json.dump(data, o, indent=4)

    # aktualizace konfiguracniho souboru
    def update_configuration(self):
        shown_text.delete("1.0", "end")
        text_file = open(self.output_configuration_file, 'r')
        stuff = text_file.read()

        shown_text.insert(END, stuff)
        text_file.close()


if __name__ == '__main__':
    Main()
