from customtkinter import *
import client
import os
import json
import popup
from PIL import Image
import picPopUp
import citywindow
import threading
import time
import os
import random
import booking
import infoPopup

from image import *
clear = lambda: os.system('cls')

class Empty(object):
    pass

data = Empty()

def loadSettings():
    data.settings = {} # Set
    with open("assets/settings.json", "r+") as file:
        temp = json.loads(file.read())
        for i in temp:
            data.settings[i] = temp[i]
    set_default_color_theme(data.settings["themeColor"])
    set_appearance_mode(data.settings["darkmode"]) # Kann nur VOR dem Erstellen des Fensters aufgerufen werden
    
def setSettings(settings, app):
    app.screens[5].items[1].set(str(settings["autoLogin"]))
    app.screens[5].items[3].set(settings["darkmode"])
    app.screens[5].items[5].set(settings["themeColor"])
    app.screens[5].items[7].set(settings["picLoading"])    

def saveSettings(app, screen):
    restart = False
    data.settings["autoLogin"] = (screen.items[1].get() == "True")
    data.settings["darkmode"] = screen.items[3].get()
    if data.settings["themeColor"] != screen.items[5].get():
        restart = True
    data.settings["themeColor"] = screen.items[5].get()
    data.settings["picLoading"] = screen.items[7].get()
    with open("assets/settings.json", "w+") as file:
        file.write(json.dumps(data.settings))
    set_appearance_mode(data.settings["darkmode"])
    if restart:
        popup.Popup("Änderungen Übernommen!\nTheme Color wird beim nächsten Start geändert!", app.returnCoords(popup.size))
    else:
        popup.Popup("Änderungen Übernommen!", app.returnCoords(popup.size))

def openInfoPopup(app, key):
    text = "Übersicht"
    daten = []
    uniqKeyItems = set()

    if key == "meerart":
        text = "Verfügbare Meerarten:"
        for i in range(len(data.data)):
            uniqKeyItems.add(data.data[i][key])
        for i in uniqKeyItems:
            bundle = {}
            bundle["text"] = i
            daten.append(bundle)
    elif key == "uebernachtungen":
        text = "Dir werden Reisen mit +2/-2 Übernachtungen angezeigt"
    elif key == "staedte":
        text = "Hier werden jene Städte angezeigt, welche zum jeweiligen Meer passen."
        if data.filter["meerart"] == "Beliebig":
            for i in range(len(data.data)):
                uniqKeyItems.update(data.data[i]["staedte"])
        else:
            for i in range(len(data.data)):
                if data.data[i]["meerart"] == data.filter["meerart"]:
                    uniqKeyItems.update(data.data[i]["staedte"])
        sorted_cities = sorted(list(uniqKeyItems))
        for i in sorted_cities:
            bundle = {}
            bundle["text"] = i
            if i in data.dataPictures.stadt:
                randCityPic = random.randint(0,max(len(data.dataPictures.stadt[i])-1,0))
                bundle["pic"] = resizePic(data.dataPictures.stadt[i][randCityPic], (400,300))
            daten.append(bundle)
    elif key == "schiffstyp":
        text = "Verfügbare Schiffsarten:"
        for i in range(len(data.data)):
            uniqKeyItems.add(data.data[i][key])
        sorted_ships = sorted(list(uniqKeyItems))
        for i in sorted_ships:
            bundle = {}
            i = "Schiffstyp " + i
            bundle["text"] = i
            if i in data.dataPictures.schiff:
                bundle["pic"] = resizePic(data.dataPictures.schiff[i], (400,300))
            daten.append(bundle)
    infoPopup.InfoPopup(text=text, curr=data.filter[key], data=daten, coords=app.returnCoords(infoPopup.size))

def waitCloseCityWindow(app, cityVar):
    global data
    while not (app.cityWindow is None or not app.cityWindow.winfo_exists()):
        time.sleep(0.1)
    cityData = json.loads(cityVar.get())
    oldCityData = data.filter["staedte"]
    if len(cityData) > 0:
        data.filter["staedte"] = cityData
    else:
        data.filter["staedte"] = ["Beliebig"]
    if oldCityData != data.filter["staedte"]:
        updateFilter(app, "staedte",True)

def openCityPopup(app):
    global data
    if app.cityWindow is None or not app.cityWindow.winfo_exists():
        cities = set()
        sorted_cities = ["Beliebig"]
        if data.filter["meerart"] == "Beliebig":
            for i in range(len(data.data)):
                cities.update(data.data[i]["staedte"])
        else:
            for i in range(len(data.data)):
                if data.data[i]["meerart"] == data.filter["meerart"]:
                    cities.update(data.data[i]["staedte"])
        sorted_cities += sorted(list(cities))
        cityVar = StringVar()
        cityVar.set(json.dumps(data.filter["staedte"]))
        app.cityWindow = citywindow.CityPopup(cities=sorted_cities,cityVar=cityVar, selected=data.filter["staedte"],coords=app.returnCoords(citywindow.size))
        threading.Thread(target=waitCloseCityWindow, args=(app, cityVar)).start()
    else:
        app.cityWindow.focus()

def waitCloseProfilPicture(app, currentProfilPicture):
    while not (app.picWindow is None or not app.picWindow.winfo_exists()):
        time.sleep(0.1)
    data.userdata["picnr"] = currentProfilPicture.get()
    updateUserData(app)
    client.updateUserData(data.userdata,app)

def updateProfilPicture(app):
    global data
    if app.picWindow is None or not app.picWindow.winfo_exists():
        currentProfilPicture = StringVar()
        currentProfilPicture.set(data.userdata["picnr"])
        app.picWindow = picPopUp.PicPopup(pics=data.profilPictures, curr=currentProfilPicture,coords=app.returnCoords(picPopUp.size))
        threading.Thread(target=waitCloseProfilPicture, args=(app, currentProfilPicture)).start()
    else:
        app.picWindow.focus()

def updateUserData(app):
    global data
    app.screens[4].items[11].configure(image=CTkImage(light_image=data.profilPictures[str(data.userdata["picnr"])], size=((100, 100))))
    app.screens[6].items[4].configure(image=CTkImage(light_image=data.profilPictures[str(data.userdata["picnr"])], size=((100, 100))))

    app.screens[4].items[14].configure(text=data.userdata["realName"])
    app.screens[4].items[15].configure(text="{} €".format(data.userdata["money"]))

    app.screens[6].items[1].configure(text=data.userdata["realName"])
    app.screens[6].items[2].configure(text="{} €".format(data.userdata["money"]))

    # screen 7 anpassen
    #
    #
    for i in range(len(app.tempBuchungen)):
        app.tempBuchungen[i].grid_forget()
    app.tempBuchungen.clear()
    for i in range(len(data.userdata["booking"])):
        if data.userdata["booking"][i] != None:
            frame = CTkFrame(master=app.screens[7].items[0])
            nr = CTkLabel(master=frame, text="ID: {}".format(data.userdata["booking"][i]["reisenummer"]))
            datum = CTkLabel(master=frame, text="Von: {}\nBis: {}".format(data.userdata["booking"][i]["datum"][0], data.userdata["booking"][i]["datum"][1]))
            preis = CTkLabel(master=frame, text="{} €".format(data.userdata["booking"][i]["preis"]))
            info = CTkButton(master=frame, text="", command=lambda: infoBooking(data.userdata["booking"][i], app), image=CTkImage(light_image=data.pictures["info"], size=((20, 20))), width=20)
            delete = CTkButton(master=frame, text="Stornieren", command=lambda: deleteBooking(data.userdata["booking"][i], app), image=CTkImage(light_image=data.pictures["delete"], size=((20, 20))), width=20)
            nr.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
            datum.grid(row=0, column=1, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
            preis.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
            info.grid(row=0, column=3, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
            delete.grid(row=0, column=4, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
            frame.columnconfigure(0, weight=1)
            frame.columnconfigure(1, weight=1)
            frame.columnconfigure(2, weight=1)

            frame.grid(row=i, column=0, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
            app.tempBuchungen.append(frame)
        
def deleteBooking(reise, app):
    if client.deleteBooking(reise):
        updateUserData(app)
        popup.Popup(text="Reise wurde gelöscht",coords=app.returnCoords(popup.size))
    else:
        popup.Popup(text="Fehler beim Löschen der Reise",coords=app.returnCoords(popup.size))

def infoBooking(reise, app):
    daten = []
    daten.append({"text": "ID: \t\t{}".format(reise["reisenummer"])})
    daten.append({"text": "Städte: \t\t{}".format("".join(str(x + ", ") for x in reise["staedte"]))})
    daten.append({"text": "Meerart: \t\t{}".format(reise["meerart"])})
    daten.append({"text": "Übernachtungen: \t{}".format(reise["uebernachtungen"])})
    daten.append({"text": "Schiffstyp: \t{}".format(reise["schiffstyp"])})
    daten.append({"text": "Kabine: \t\t{}".format(reise["kabine"])})
    daten.append({"text": "Datum: \t\tvon {} \tbis {}".format(reise["datum"][0],reise["datum"][1])})
    daten.append({"text": "Preis: \t\t{} €".format(reise["preis"])})
    info = infoPopup.InfoPopup(text="Informationen zur gebuchten Reise", data=daten, coords=app.returnCoords(infoPopup.size))
    info.setSize((800, 500))

def asyncPicLoading(pics=[]):
    for i in range(len(pics)):
        newPic = resizePic(pics[i][1], (200,200))
        pics[i][0].configure(text="",image=CTkImage(light_image=newPic, size=((newPic.size[0], newPic.size[1]))))

def updateFilter(app, type, val=0):
    global data
    temp = []
    if data.filter[type] != val and val != 0:
        data.filter["meerart"] = app.screens[4].items[3].get()
        data.filter["uebernachtungen"] = app.screens[4].items[4].get()
        data.filter["schiffstyp"] = app.screens[4].items[6].get()
        if type == "meerart":
            data.filter["staedte"] = ["Beliebig"]
        for i in range(len(data.data)):
            if not(data.filter["meerart"] == "Beliebig" or data.data[i]["meerart"] == data.filter["meerart"]):
                continue
            if not(data.filter["uebernachtungen"] == "Beliebig" or (data.data[i]["uebernachtungen"] >= data.filter["uebernachtungen"] -2 and data.data[i]["uebernachtungen"] <= data.filter["uebernachtungen"] + 2 )):
                continue
            if  not "Beliebig" in data.filter["staedte"]:
                exists = False
                for j in data.filter["staedte"]:
                    if not j in data.data[i]["staedte"]:
                        exists = True
                        break
                if exists:
                    continue
            if not(data.filter["schiffstyp"] == "Beliebig" or data.data[i]["schiffstyp"] == data.filter["schiffstyp"]):
                continue
            temp.append(data.data[i])
        for i in range(len(app.results)):
            app.results[i].grid_forget()
        app.results.clear()
        tempPics = []
        for i in range(len(temp)):
            frame = CTkFrame(master=app.screens[4].items[2])
            cities = random.choice(temp[i]["staedte"])

            while not cities in  data.dataPictures.stadt: # Es gibt Städte ohne Bilder
                cities = random.choice(temp[i]["staedte"])
            randCityPic = random.randint(0,max(len(data.dataPictures.stadt[cities])-1,0))
            
            if data.settings["picLoading"] == "synchronisiert":
                newPic = resizePic(data.dataPictures.stadt[cities][randCityPic], (200,200)) # Wird ausgelagert -> Asynchron
                pic = CTkLabel(master=frame, text="", image=CTkImage(light_image=newPic, size=((newPic.size[0], newPic.size[1]))))
            else:
                pic = CTkLabel(master=frame, text="Bild wird geladen", width=200, height=200)
                tempPics.append((pic, data.dataPictures.stadt[cities][randCityPic]))
            pic.grid(row=0, column=0,rowspan=4,padx=10, pady=10,sticky=N+S+E+W)
            
            meerartstr = ""
            meerartsplit = temp[i]["meerart"].split()
            for j in range(len(meerartsplit)):
                if j % 3 == 0:
                    if j > 0:
                        meerartstr += "\n"
                    meerartstr += meerartsplit[j]
                    if j + 1 < len(meerartsplit):
                        meerartstr += " "
                else:
                    meerartstr += meerartsplit[j]
                    if j + 1 < len(meerartsplit):
                        meerartstr += " "
            meerart = CTkLabel(frame, text=meerartstr)
            meerart.grid(row=0, column=1, pady=10,sticky=N+S+E+W)

            uebernachtungen = CTkLabel(frame, text="{} Übernachtungen".format(temp[i]["uebernachtungen"]))
            uebernachtungen.grid(row=1, column=1, pady=10,sticky=N+S+E+W)

            staedtestr = ""
            for j in range(len(temp[i]["staedte"])):
                if j % 2 == 0:
                    if j > 0:
                        staedtestr += "\n"
                    staedtestr += temp[i]["staedte"][j]
                    if j + 1 < len(temp[i]["staedte"]):
                        staedtestr += ", "
                else:
                    staedtestr += temp[i]["staedte"][j]
            staedte = CTkLabel(frame, text=staedtestr)
            staedte.grid(row=2, column=1, padx=10, pady=10)

            schiffstyp = CTkLabel(frame, text="Schiffstyp {}".format(temp[i]["schiffstyp"]))
            schiffstyp.grid(row=3, column=1, pady=10,sticky=N+S+E+W)

            preisspanne = [0,0] # min max
            for j in range(len(temp[i]["kabinen"])):
                if j == 0:
                    preisspanne = [temp[i]["kabinen"][0]["price"],temp[i]["kabinen"][0]["price"]]
                if preisspanne[0] > temp[i]["kabinen"][j]["price"]:
                    preisspanne[0] = temp[i]["kabinen"][j]["price"]
                if preisspanne[1] < temp[i]["kabinen"][j]["price"]:
                    preisspanne[1] = temp[i]["kabinen"][j]["price"]
            
            if preisspanne[0] == preisspanne[1]:
                preis = CTkLabel(frame, text="{}€".format(preisspanne[0]))
            else:
                preis = CTkLabel(frame, text="{}€ - {}€".format(preisspanne[0], preisspanne[1]))
            preis.grid(row=0, column=2, rowspan=2, padx=10, pady=10,sticky=N+S+E+W)


            nr = CTkLabel(frame, text="Nr {}".format(temp[i]["reisenummer"]))
            nr.grid(row=2, column=2, padx=10, pady=10,sticky=N+S+E+W)

            buchenButton = CTkButton(master=frame, text="Buchen")
            if preisspanne[0] > data.userdata["money"]:
                buchenButton.configure(command=lambda: popup.Popup(text="Du hast nicht genug Geld,\num dir diese Reise leisten zu können!",coords=app.returnCoords(popup.size)))
            else:
                buchenButton.configure(command=lambda x=temp[i]: openBooking(app,x))
            buchenButton.grid(row=3, column=2,padx=10, pady=10,sticky=N+S+E+W)

            frame.rowconfigure(0, weight=1)
            frame.rowconfigure(1, weight=1)
            frame.rowconfigure(2, weight=1)
            frame.rowconfigure(3, weight=1)
            frame.columnconfigure(1, weight=1)

            frame.grid(row=i-i%2, column=i%2, padx=10, pady=10,sticky=N+S+E+W)
            app.results.append(frame)
        if data.settings["picLoading"] == "asynchron":
            threading.Thread(target=asyncPicLoading, args=([tempPics])).start()

def waitCloseBookingWindow(app, bookingVar):
    global data
    while not (app.bookingWindow is None or not app.bookingWindow.winfo_exists()):
        time.sleep(0.1)
    bookingData = json.loads(bookingVar.get())
    if bookingData != None:
        if client.book(bookingData):
            popup.Popup(text="Reise wurde erfolgreich gebucht",coords=app.returnCoords(popup.size))
            updateUserData(app)
        else:
            popup.Popup(text="Server Error! Reise konnte nicht gebucht werden",coords=app.returnCoords(popup.size))
    else:
        popup.Popup(text="Fehler bei der Buchungsauswahl",coords=app.returnCoords(popup.size))

def openBooking(app,reise):
    global data
    if app.bookingWindow is None or not app.bookingWindow.winfo_exists():
        bookingVar = StringVar()
        bookingVar.set(json.dumps(None))
        pics = {}
        pics["schiffstyp"] = data.dataPictures.schiff["{} {}".format("Schiffstyp",reise["schiffstyp"])]
        pics["staedte"] = {}
        for i in data.dataPictures.stadt:
            if i in reise["staedte"]:
                pics["staedte"][i] = data.dataPictures.stadt[i]
        pics["kabine"] = data.dataPictures.kabine
        app.bookingWindow = booking.BookingPopup(reise, bookingVar,pics, money=data.userdata["money"],infoicon=data.pictures["info"], coords=app.returnCoords(booking.size))
        threading.Thread(target=waitCloseBookingWindow, args=(app, bookingVar)).start()
    else:
        app.bookingWindow.focus()

def loadingFiles(status: StringVar, app):
    global data
    data.version = "0.0"
    status.set("Loading Version")
    if len(os.listdir("data")) > 0: # Leerer Ordner -> Fragt nach Daten (Bsp erster Start)
        with open("assets/VERSION", "r") as file:
            data.version = file.read()
    status.set("Authentification")
    data.auth = Empty() # Nur für Autologin
    data.auth.username = ""
    data.auth.password = ""
    if data.settings["autoLogin"]:
        with open("assets/userdata.json", "r+") as file:
            temp = json.loads(file.read())
            data.auth.username = temp["username"]
            data.auth.password = temp["password"]
    data.userdata = {} # Alle Userdaten
    data.pictures = {} # Icons
    for path in os.listdir("assets/pics"):
        filename = os.path.join("assets/pics", path)
        if os.path.isfile(filename):
            data.pictures[os.path.splitext(path)[0]] = Image.open(filename)
    data.profilPictures = {} # Profilpics
    for path in os.listdir("assets/profilpics"):
        filename = os.path.join("assets/profilpics", path)
        if os.path.isfile(filename):
            data.profilPictures[os.path.splitext(path)[0]] = Image.open(filename)
    data.filter = {}
    data.filter["staedte"] = ["Beliebig"]
    data.filter["meerart"] = "Beliebig"
    data.filter["uebernachtungen"] = "Beliebig"
    data.filter["schiffstyp"] = "Beliebig"
    
    client.connectStart(data.version, status, app)
    
    data.data = []
    with open("data/reisen.json", encoding='utf-8') as file:
        data.data = json.loads(file.read())
    data.dataPictures = Empty()
    data.dataPictures.kabine = {}
    data.dataPictures.schiff = {}
    data.dataPictures.stadt = {}
    for path in os.listdir("data/kabine"):
        filename = os.path.join("data/kabine", path)
        if os.path.isfile(filename):
            data.dataPictures.kabine[os.path.splitext(path)[0]] = Image.open(filename)
    for path in os.listdir("data/schiff"):
        filename = os.path.join("data/schiff", path)
        if os.path.isfile(filename):
            data.dataPictures.schiff[os.path.splitext(path)[0]] = Image.open(filename)
    for path in os.listdir("data/stadt"):
        filename = os.path.join("data/stadt", path)
        name = os.path.splitext(path)[0].replace("_"," ")
        if os.path.isfile(filename):
            if name in  data.dataPictures.stadt:
                data.dataPictures.stadt[name].append(Image.open(filename))
            else:
                data.dataPictures.stadt[name] = [Image.open(filename)]

    setSettings(data.settings, app)
    updateUserData(app)
    app.screens[4].items[12].configure(image=CTkImage(light_image=data.pictures["settings"], size=((30, 30))))
    app.screens[4].items[13].configure(image=CTkImage(light_image=data.pictures["history"], size=((30, 30))))
    app.screens[4].items[16].configure(image=CTkImage(light_image=data.pictures["info"], size=((20, 20))))
    app.screens[4].items[17].configure(image=CTkImage(light_image=data.pictures["info"], size=((20, 20))))
    app.screens[4].items[18].configure(image=CTkImage(light_image=data.pictures["info"], size=((20, 20))))
    app.screens[4].items[19].configure(image=CTkImage(light_image=data.pictures["info"], size=((20, 20))))
    app.screens[6].items[3].configure(image=CTkImage(light_image=data.pictures["history"], size=((20, 20))))