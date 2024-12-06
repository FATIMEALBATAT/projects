from customtkinter import *
import json
size = (600, 400)

# Popup für Kleine Infos
class CityPopup(CTkToplevel):
    def __init__(self, cities, cityVar, selected,coords=(100,100),*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("{}x{}".format(size[0], size[1])) # Fenstergröße
        self.geometry("+{}+{}".format(coords[0], coords[1])) # Position des Fensters
        self.title("Städte auswählen")
        self.resizable(False,False)
        self.attributes("-topmost", 3)
        self.items = []
        self.rows = 0
        self.columns = 0
        self.scroll = CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.grid(row=0, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.scroll.columnconfigure(0, weight=1)
        self.scroll.columnconfigure(1, weight=1)
        self.scroll.columnconfigure(2, weight=1)
        self.data = ""
        self.checkboxes = []
        self.cityVar = cityVar
        for i in cities:
            frame = CTkFrame(self.scroll)
            self.items.append(frame)
            checkbox = CTkCheckBox(frame,text=i, command=lambda x=i: self.update(x))
            if i in selected:
                checkbox.select()
            checkbox.grid(row=0, column=0,padx=10, pady=10, sticky=N+E+S+W)
            self.checkboxes.append(checkbox)
        for i in range(len(self.items)):
            if self.columns == 0:
                self.rows += 1
            self.items[i].grid(row=self.rows, column=self.columns, columnspan=1, padx=10, pady=10,sticky=N+E+S+W)
            self.columns = (self.columns + 1) % 3
        self.after(100, self.lift)
    def update(self, val):
        temp = []
        if val == "Beliebig":
            for i in range(len(self.checkboxes)):
                if self.checkboxes[i].get() and self.checkboxes[i].cget("text") != "Beliebig":
                    self.checkboxes[i].deselect()
        else:
            self.checkboxes[0].deselect()
        for i in range(len(self.checkboxes)):
            if self.checkboxes[i].get():
                temp.append(self.checkboxes[i].cget("text"))
        self.cityVar.set(json.dumps(temp))