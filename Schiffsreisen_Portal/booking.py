from customtkinter import *
import tkcalendar
import datetime
import json
import popup
import infoPopup
import image
import random

size = (800, 600)

# Popup für Kleine Infos
class BookingPopup(CTkToplevel):
    def __init__(self, reise, bookingVar: StringVar, pics, money, infoicon, coords=(100,100),*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("{}x{}".format(size[0], size[1])) # Fenstergröße
        self.geometry("+{}+{}".format(coords[0], coords[1])) # Position des Fensters
        self.resizable(False,False)
        self.attributes("-topmost", 2)
        self.title("Buchungsfenster")
        self.scroll = CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.grid(row=0, column=0, columnspan=2,padx=10, pady=10, sticky=N+E+S+W)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.scroll.columnconfigure(0, weight=1)
        self.scroll.columnconfigure(1, weight=1)
        self.scroll.columnconfigure(2, weight=1)
        self.bookingVar = bookingVar
        self.tempData = None
        self.data = reise
        self.items = []
        self.money = money
        self.coords = coords
        self.kabineWindow = None
        self.pics = pics
        self.date = [datetime.date.today(), datetime.date.today() + datetime.timedelta(reise["uebernachtungen"])] # start | end

        # Wann
        wann = CTkFrame(self.scroll)
        wann.columnconfigure(0, weight=1)
        wann.columnconfigure(1, weight=1)
        self.items.append(wann)
        self.items[0].grid(row=0, column=0, columnspan=3,padx=10, pady=10, sticky=N+E+S+W)
        self.items.append(CTkLabel(wann, text="Wann ?"))
        self.items.append(CTkLabel(wann, text="Von"))
        self.items.append(CTkLabel(wann, text="Bis"))
        self.items.append(tkcalendar.DateEntry(wann, justify="center",mindate=datetime.date.today(),date_pattern='dd-MM-yyyy'))
        self.items[4].bind("<<DateEntrySelected>>", self.updateDate) # weil command=... nicht geht
        endday = datetime.date.today() + datetime.timedelta(reise["uebernachtungen"])
        self.items.append(CTkLabel(wann, text="{}-{}-{}".format(endday.day, endday.month, endday.year)))

        self.items[1].grid(row=0, column=0, columnspan=2,padx=10, pady=10, sticky=N+E+S+W)
        self.items[2].grid(row=1, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[3].grid(row=1, column=1, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[4].grid(row=2, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[5].grid(row=2, column=1, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)

        # kabine
        kabine = CTkFrame(self.scroll)
        kabine.columnconfigure(0, weight=1)
        kabine.columnconfigure(1, weight=1)
        kabine.columnconfigure(3, weight=1)
        self.items.append(kabine)
        self.items[6].grid(row=1, column=0, columnspan=3,padx=10, pady=10, sticky=N+E+S+W)
        self.items.append(CTkLabel(kabine, text="Kabinenauswahl"))

        kabinenliste = []
        for i in range(len(reise["kabinen"])):
            kabinenliste.append(reise["kabinen"][i]["type"])

        self.items.append(CTkOptionMenu(kabine,values=kabinenliste, command=lambda x: self.updateKabine(x)))
        self.items.append(CTkButton(kabine, text="", width=20, image=CTkImage(light_image=infoicon, size=((20, 20))), command=self.openInfoKabine))
        self.items[7].grid(row=0, column=1, columnspan=2,padx=10, pady=10, sticky=N+E+S+W)
        self.items[8].grid(row=1, column=1, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[9].grid(row=1, column=2, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)

        # Zusammenfassung
        summary = CTkFrame(self.scroll)
        summary.columnconfigure(0, weight=1)
        summary.columnconfigure(2, weight=2)
        self.items.append(summary)
        self.items[10].grid(row=2, column=0, columnspan=3,padx=10, pady=10, sticky=N+E+S+W)
        self.items.append(CTkLabel(summary, text="Zusammenfassung"))
        self.items.append(CTkLabel(summary, text="Reise ID:"))
        self.items.append(CTkLabel(summary, text=reise["reisenummer"]))
        self.items.append(CTkLabel(summary, text="Meerart"))
        self.items.append(CTkLabel(summary, text=reise["meerart"]))
        self.items.append(CTkLabel(summary, text="Übernachtungen"))
        self.items.append(CTkLabel(summary, text=reise["uebernachtungen"]))
        self.items.append(CTkLabel(summary, text="Städte"))
        self.items.append(CTkButton(summary, text="", width=20, command=lambda: self.openInfoStaedteSummary(reise["staedte"], pics["staedte"]),image=CTkImage(light_image=infoicon, size=((20, 20)))))
        self.items.append(CTkLabel(summary, text=reise["staedte"]))
        self.items.append(CTkLabel(summary, text="Schiffstyp"))
        self.items.append(CTkButton(summary, text="", width=20, command=lambda: infoPopup.InfoPopup(text="Schiffstyp", data=[{"text": "Schiffstyp {}".format(reise["schiffstyp"]),"pic":pics["schiffstyp"]}], coords=self.coords),image=CTkImage(light_image=infoicon, size=((20, 20)))))
        self.items.append(CTkLabel(summary, text=reise["schiffstyp"]))
        self.items.append(CTkLabel(summary, text="Kabinentyp"))
        self.items.append(CTkButton(summary, text="", width=20,command=self.openInfoKabineSummary,image=CTkImage(light_image=infoicon, size=((20, 20)))))
        self.items.append(CTkLabel(summary, text="..."))
        self.items.append(CTkLabel(summary, text="Gesamtpreis"))
        self.items.append(CTkLabel(summary, text="... €"))

        self.items[11].grid(row=0, column=0, columnspan=3,padx=10, pady=10, sticky=N+E+S+W)
        self.items[12].grid(row=1, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[13].grid(row=1, column=2, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[14].grid(row=2, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        
        self.items[15].grid(row=2, column=2, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[16].grid(row=3, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        
        self.items[17].grid(row=3, column=2, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[18].grid(row=4, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[19].grid(row=4, column=1, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[20].grid(row=4, column=2, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[21].grid(row=5, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[22].grid(row=5, column=1, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[23].grid(row=5, column=2, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[24].grid(row=6, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[25].grid(row=6, column=1, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[26].grid(row=6, column=2, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.items[27].grid(row=7, column=0, columnspan=2,padx=10, pady=10, sticky=N+E+S+W)
        self.items[28].grid(row=7, column=2, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)

        warning = CTkFrame(self.scroll, fg_color="red")
        warning.columnconfigure(0, weight=1)
        warning.columnconfigure(1, weight=2)
        self.items.append(warning)
        self.items.append(CTkLabel(warning, text="Hinweis!"))
        self.items.append(CTkLabel(warning, text="Sie haben nicht genug Guthaben, um diese Reise zu buchen!"))
        self.items[29].grid(row=3, column=0, columnspan=3,padx=10, pady=10, sticky=N+E+S+W)

        self.items[30].grid(row=0, column=0, columnspan=2,padx=10, pady=10, sticky=N+E+S+W)
        self.items[31].grid(row=1, column=0, columnspan=2,padx=10, pady=10, sticky=N+E+S+W)

        self.items.append(CTkButton(self.scroll, text="Buchen", command=lambda: self.update(kabine=self.items[8].get())))
        self.items[32].grid(row=4, column=1, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.after(100, self.lift)
        self.updateKabine(self.items[8].get())
    def openInfoStaedteSummary(self, staedte, pics):
        daten = []
        for i in range(len(staedte)):
            bundle = {}
            bundle["text"] = staedte[i]
            if staedte[i] in pics:
                randCityPic = random.randint(0,max(len(pics[staedte[i]])-1,0))
                bundle["pic"] = image.resizePic(pics[staedte[i]][randCityPic], (400,300))
            daten.append(bundle)
        infoPopup.InfoPopup(text="Städtetour", data=daten, coords=self.coords)
    def openInfoKabineSummary(self):
        text = "Ausgewählte Kabine"
        daten = []
        name = self.items[8].get()
        if "Luxuskabine" in name:
            temp = name.split(" ")
            name = "{} Kategorie {}".format(temp[0],temp[1])
        if name in self.pics["kabine"]:
            bundle = {}
            bundle["text"] = name
            bundle["pic"] = image.resizePic(self.pics["kabine"][name], (400,300))
            daten.append(bundle)
        infoPopup.InfoPopup(text=text, data=daten, coords=self.coords)
    def openInfoKabine(self):
        if self.kabineWindow is None or not self.kabineWindow.winfo_exists():
            text = "Verfügbare Kabinen:"
            daten = []
            for i in range(len(self.data["kabinen"])):
                name = self.data["kabinen"][i]["type"]
                if "Luxuskabine" in name:
                    temp = name.split(" ")
                    name = "{} Kategorie {}".format(temp[0],temp[1])
                if name in self.pics["kabine"]:
                    bundle = {}
                    bundle["text"] = name
                    bundle["pic"] = image.resizePic(self.pics["kabine"][name], (400,300))
                    daten.append(bundle)
            self.kabineWindow = infoPopup.InfoPopup(text=text, curr=self.items[8].get(), data=daten, coords=self.coords)
        else:
            self.kabineWindow.focus()
    def updateKabine(self, kabine):
        daten = []
        for i in range(len(self.data["kabinen"])):
            if kabine == self.data["kabinen"][i]["type"]:
                name = self.data["kabinen"][i]["type"]
                if "Luxuskabine" in name:
                    temp = name.split(" ")
                    name = "{} Kategorie {}".format(temp[0],temp[1])
                self.items[28].configure(text="{} €".format(self.data["kabinen"][i]["price"]))
                if name in self.pics["kabine"]:
                    bundle = {}
                    bundle["text"] = name
                    bundle["pic"] = image.resizePic(self.pics["kabine"][name], (400,300))
                    daten.append(bundle)
                self.items[26].configure(text=kabine)

                if self.data["kabinen"][i]["price"] > self.money:
                    self.items[32].configure(state="disabled")
                    self.items[29].grid(row=3, column=0, columnspan=2,padx=10, pady=10, sticky=N+E+S+W)
                else:
                    self.items[32].configure(state="normal")
                    self.items[29].grid_forget()
                break
    def updateDate(self, event):
        w = event.widget
        date = w.get_date()
        endday = date + datetime.timedelta(self.data["uebernachtungen"])
        self.items[5].configure(text="{}-{}-{}".format(endday.day, endday.month, endday.year))
        self.date = [date, endday]
    def update(self, kabine = ""):
        if kabine is not None:
            self.tempData = {}
            self.tempData["staedte"] = self.data["staedte"]
            self.tempData["preis"] = -1
            self.tempData["reisenummer"] = self.data["reisenummer"]
            self.tempData["meerart"] = self.data["meerart"]
            self.tempData["uebernachtungen"] = self.data["uebernachtungen"]
            self.tempData["schiffstyp"] = self.data["schiffstyp"]
            self.tempData["kabine"] = kabine
            self.tempData["datum"] = [self.date[0].strftime("%d-%m-%Y"),self.date[1].strftime("%d-%m-%Y")]
            for i in range(len(self.data["kabinen"])):
                if kabine == self.data["kabinen"][i]["type"]:
                    self.tempData["preis"] = self.data["kabinen"][i]["price"]
                    break
            if self.tempData["preis"] != -1:
                self.bookingVar.set(json.dumps(self.tempData))
                self.destroy()
            else:
                popup.Popup(text="Preis konnte nicht ermittelt werden.", coords=self.coords)