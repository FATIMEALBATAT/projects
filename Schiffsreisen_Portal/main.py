from customtkinter import *
import client
import threading
import files
import window
from spinbox import *
from PIL import Image

def loadingAll(app, loadingStatus):
    files.loadingFiles(loadingStatus, app)
    if client.updated == False:
        app.switchScreen(1) # switch to Error screen
    else:
        app.switchScreen(4) # switch to Main screen
        files.updateFilter(app, "staedte",True)

def toggle_password(entry):
    if entry.cget('show') == '':
        entry.configure(show='*')
    else:
        entry.configure(show='')

def main():
    placeholder_image = CTkImage(light_image=Image.open("assets/placeholder.png"),size=(1, 1))

    app = window.Window()
    
    app.addScreen("Schiffsreisenplaner - Loading", (400,200))
    loadingVar = StringVar(value="Loading ...")
    app.screens[0].items.append(CTkLabel(master=app.screens[0], textvariable=loadingVar))
    app.screens[0].items[0].grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[0].columnconfigure(0, weight=1)
    app.screens[0].columnconfigure(2, weight=1)
    app.screens[0].rowconfigure(0, weight=1)
    app.screens[0].rowconfigure(2, weight=1)

    app.addScreen("Schiffsreisenplaner - Keine Netzwerkverbindung!", (400,200))
    app.screens[1].items.append(CTkLabel(master=app.screens[1], text="Keine Netzwerkverbindung!"))
    app.screens[1].items.append(CTkButton(app.screens[1], text="Trotzdem rumstöbern", command=lambda: app.switchScreen(4)))
    app.screens[1].items[0].grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[1].items[1].grid(row=2, column=1, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[1].columnconfigure(0, weight=1)
    app.screens[1].columnconfigure(2, weight=1)
    app.screens[1].rowconfigure(0, weight=1)
    app.screens[1].rowconfigure(3, weight=1)

    app.addScreen("Schiffsreisenplaner - Login", (600,300), True)
    app.screens[2].items.append(CTkLabel(master=app.screens[2], text="Login"))
    app.screens[2].items.append(CTkEntry(app.screens[2], placeholder_text="Username"))
    app.screens[2].items.append(CTkEntry(app.screens[2], placeholder_text="Password"))
    toggle_password(app.screens[2].items[2])
    app.screens[2].items.append(CTkButton(app.screens[2], text="Login", command=lambda: client.updateLoginData(app)))
    app.screens[2].items.append(CTkButton(app.screens[2], text="Register", command=lambda: app.switchScreen(3)))
    app.screens[2].items[0].grid(row=1, column=1, columnspan=5, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[2].items[1].grid(row=3, column=1, columnspan=5, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[2].items[2].grid(row=5, column=1, columnspan=5, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[2].items[3].grid(row=7, column=1, columnspan=2, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[2].items[4].grid(row=7, column=4, columnspan=2, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[2].columnconfigure(3, weight=1)
    app.screens[2].columnconfigure(0, weight=1)
    app.screens[2].columnconfigure(7, weight=1)
    app.screens[2].rowconfigure(0, weight=1)
    app.screens[2].rowconfigure(8, weight=1)

    app.addScreen("Schiffsreisenplaner - Register", (600,400))
    app.screens[3].items.append(CTkLabel(master=app.screens[3], text="Register"))
    app.screens[3].items.append(CTkEntry(app.screens[3], placeholder_text="Ihr Name"))
    app.screens[3].items.append(CTkEntry(app.screens[3], placeholder_text="Benutzername"))
    app.screens[3].items.append(CTkEntry(app.screens[3], placeholder_text="Passwort"))
    app.screens[3].items.append(CTkEntry(app.screens[3], placeholder_text="Passwort wiederholen"))
    app.screens[3].items.append(CTkButton(app.screens[3], text="Registrieren", command=lambda: client.register(app)))
    app.screens[3].items.append(CTkButton(app.screens[3], text="Abbruch", command=lambda: app.switchScreen(2)))
    app.screens[3].items[0].grid(row=1, column=1, columnspan=5, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[3].items[1].grid(row=3, column=1, columnspan=5, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[3].items[2].grid(row=5, column=1, columnspan=5, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[3].items[3].grid(row=7, column=1, columnspan=5, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[3].items[4].grid(row=9, column=1, columnspan=5, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[3].items[5].grid(row=11, column=1, columnspan=2, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[3].items[6].grid(row=11, column=4, columnspan=2, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[3].columnconfigure(3, weight=1)
    app.screens[3].columnconfigure(0, weight=1)
    app.screens[3].columnconfigure(7, weight=1)
    app.screens[3].rowconfigure(0, weight=1)
    app.screens[3].rowconfigure(12, weight=1)

    app.addScreen("Schiffsreisenplaner - Filter", (1400,650))
    #app.screens[4].items.append(CTkLabel(master=app.screens[4], text="Hauptscreen"))
    app.screens[4].items.append(CTkFrame(master=app.screens[4]))
    app.screens[4].items[0].grid(column=0,row=0,padx=(10,0), pady=10, sticky=N+S+E+W)
    #Frame - Profil - Oben Rechts
    app.screens[4].items.append(CTkFrame(master=app.screens[4]))
    app.screens[4].items[1].grid(column=1,row=0,padx=10, pady=10,sticky=N+E+S+W)
    #Frame - SuchErgebnis - UntenMitte
    app.screens[4].items.append(CTkScrollableFrame(master=app.screens[4]))
    app.screens[4].items[2].grid(column=0,row=1,columnspan=2,padx=10, pady=(0,10),sticky=N+S+E+W)
    app.screens[4].items[2].columnconfigure(0, weight=1)
    app.screens[4].items[2].columnconfigure(1, weight=1)

    app.screens[4].items.append(CTkOptionMenu(master=app.screens[4].items[0], command=lambda val: files.updateFilter(app,"meerart",val), values=["Beliebig","Ostsee", "Nordsee", "Mittelmeer", "Nordpolarmeer"]))

    app.screens[4].items[3].grid(column=1,row=2,padx=(20,5), pady=10,sticky=N+S+E+W)
    app.screens[4].items.append(Spinbox(master=app.screens[4].items[0], app=app, command=lambda: files.updateFilter(app,"uebernachtungen",-2)))
    app.screens[4].items[4].grid(column=3,row=2,padx=(20,5), pady=10,sticky=N+S+E+W)
 
    app.screens[4].items.append(CTkButton(master=app.screens[4].items[0], text="Öffne Städteübersicht", command=lambda: files.openCityPopup(app))) #command=tete.CityWindow 
    app.screens[4].items[5].grid(column=5,row=2,padx=(20,5), pady=10,sticky=N+S+E+W)

    app.screens[4].items.append(CTkOptionMenu(master=app.screens[4].items[0], command=lambda val: files.updateFilter(app,"schiffsart",val),values=["Beliebig","A","B","C","D","E","F","G","H","I","X"]))
    app.screens[4].items[6].grid(column=7,row=2,padx=(20,5), pady=10,sticky=N+S+E+W)

    # Texte für DropDown
    app.screens[4].items.append(CTkLabel(master=app.screens[4].items[0],text="Meerart"))
    app.screens[4].items[7].grid(column=1,row=1,padx=10, pady=10,sticky=N+S+E+W)
    app.screens[4].items.append(CTkLabel(master=app.screens[4].items[0],text="Übernachtungen"))
    app.screens[4].items[8].grid(column=3,row=1,padx=10, pady=10,sticky=N+S+E+W)
    app.screens[4].items.append(CTkLabel(master=app.screens[4].items[0],text="Besuchte Städte"))
    app.screens[4].items[9].grid(column=5,row=1,padx=10, pady=10,sticky=N+S+E+W)
    app.screens[4].items.append(CTkLabel(master=app.screens[4].items[0],text="Schiff Arten"))
    app.screens[4].items[10].grid(column=7,row=1,padx=10, pady=10,sticky=N+S+E+W)

    # Allgmein Screen 0 Fenster 
    app.screens[4].columnconfigure(0, weight=1)
    app.screens[4].rowconfigure(1, weight=1)

    # Frame für Filter - Links Oben
    app.screens[4].items[0].columnconfigure(0, weight=1)
    app.screens[4].items[0].columnconfigure(1, weight=1)
    app.screens[4].items[0].columnconfigure(3, weight=1)
    app.screens[4].items[0].columnconfigure(5, weight=1)
    app.screens[4].items[0].columnconfigure(7, weight=1)
    app.screens[4].items[0].columnconfigure(9, weight=1)
    app.screens[4].items[0].rowconfigure(0, weight=1)
    app.screens[4].items[0].rowconfigure(3, weight=1)

    app.screens[4].items.append(CTkButton(master=app.screens[4].items[1],text="",image=placeholder_image,command=lambda: app.switchScreen(6), width=100))
    app.screens[4].items[11].grid(column=0,row=0,columnspan=2, rowspan=2,padx=10, pady=10)

    app.screens[4].items.append(CTkButton(master=app.screens[4].items[1],text="",image=placeholder_image,command=lambda: app.switchScreen(5), width=50, height=50))
    app.screens[4].items[12].grid(column=0,row=2, padx=10,pady=(0,10))
    app.screens[4].items.append(CTkButton(master=app.screens[4].items[1],text="",image=placeholder_image,command=lambda: app.switchScreen(7), width=50, height=50))
    app.screens[4].items[13].grid(column=1,row=2, padx=(0,10), pady=(0,10))

    app.screens[4].items.append(CTkLabel(master=app.screens[4].items[1],text="Max Mustermann", width=100))
    app.screens[4].items[14].grid(column=2,row=0,padx=10, pady=10,sticky=E)

    app.screens[4].items.append(CTkLabel(master=app.screens[4].items[1],text="100.000 €", width=100))
    app.screens[4].items[15].grid(column=2,row=1,padx=10, pady=10,sticky=E)

    app.screens[4].items[1].columnconfigure(2, weight=0)

    app.screens[4].items.append(CTkButton(master=app.screens[4].items[0],text="", command=lambda: files.openInfoPopup(app, "meerart"), image=placeholder_image,width=20))
    app.screens[4].items[16].grid(column=2,row=2,padx=(0,10), pady=10)
    app.screens[4].items.append(CTkButton(master=app.screens[4].items[0],text="", command=lambda: files.openInfoPopup(app, "uebernachtungen"), image=placeholder_image,width=20))
    app.screens[4].items[17].grid(column=4,row=2,padx=(0,10), pady=10)
    app.screens[4].items.append(CTkButton(master=app.screens[4].items[0],text="", command=lambda: files.openInfoPopup(app, "staedte"), image=placeholder_image,width=20))
    app.screens[4].items[18].grid(column=6,row=2,padx=(0,10), pady=10)
    app.screens[4].items.append(CTkButton(master=app.screens[4].items[0],text="", command=lambda: files.openInfoPopup(app, "schiffstyp"), image=placeholder_image,width=20))
    app.screens[4].items[19].grid(column=8,row=2,padx=(0,10), pady=10)

    app.addScreen("Schiffsreisenplaner - Einstellungen", (600,300))
    app.screens[5].items.append(CTkLabel(app.screens[5], text="Automatisches Einloggen"))
    app.screens[5].items.append(CTkOptionMenu(app.screens[5], values=["True", "False"]))
    app.screens[5].items.append(CTkLabel(app.screens[5], text="Darkmode"))
    app.screens[5].items.append(CTkOptionMenu(app.screens[5], values=["dark", "light", "system"]))
    app.screens[5].items.append(CTkLabel(app.screens[5], text="Theme Color"))
    app.screens[5].items.append(CTkOptionMenu(app.screens[5], values=["blue", "dark-blue", "green"]))
    app.screens[5].items.append(CTkLabel(app.screens[5], text="Bilder laden"))
    app.screens[5].items.append(CTkOptionMenu(app.screens[5], values=["synchronisiert", "asynchron"]))
    app.screens[5].items.append(CTkButton(app.screens[5], text="Zurück", command=lambda: app.switchScreen(4)))
    app.screens[5].items.append(CTkButton(app.screens[5], text="Änderungen Übernehmen", command=lambda: files.saveSettings(app, app.screens[5])))
    app.screens[5].items[0].grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[5].items[1].grid(row=1, column=2, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[5].items[2].grid(row=2, column=1, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[5].items[3].grid(row=2, column=2, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[5].items[4].grid(row=3, column=1, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[5].items[5].grid(row=3, column=2, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[5].items[6].grid(row=4, column=1, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[5].items[7].grid(row=4, column=2, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[5].items[8].grid(row=6, column=1, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[5].items[9].grid(row=6, column=2, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[5].columnconfigure(0, weight=1)
    app.screens[5].columnconfigure(3, weight=1)
    app.screens[5].rowconfigure(0, weight=1)
    app.screens[5].rowconfigure(5, weight=1)
    app.screens[5].rowconfigure(7, weight=1)

    app.addScreen("Schiffsreisenplaner - Profil", (800,500))
    app.screens[6].items.append(CTkButton(app.screens[6], text="Zurück", command=lambda: app.switchScreen(4)))
    app.screens[6].items.append(CTkLabel(app.screens[6], text="Name"))
    app.screens[6].items.append(CTkLabel(app.screens[6], text="Geld"))
    app.screens[6].items.append(CTkButton(app.screens[6], text="",image=placeholder_image, command=lambda: app.switchScreen(7), width=20))
    app.screens[6].items.append(CTkLabel(app.screens[6], text="",image=placeholder_image))
    app.screens[6].items.append(CTkButton(app.screens[6], text="Profil-Icon ändern", command=lambda: files.updateProfilPicture(app)))
    app.screens[6].items.append(CTkButton(app.screens[6], text="Abmelden", command=lambda: client.logout(app, loadingVar)))
    app.screens[6].items[0].grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[6].items[1].grid(row=2, column=3, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[6].items[2].grid(row=2, column=5, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[6].items[3].grid(row=2, column=7, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[6].items[4].grid(row=4, column=4, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[6].items[5].grid(row=5, column=4, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[6].items[6].grid(row=7, column=4, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[6].columnconfigure(1, weight=1)
    app.screens[6].columnconfigure(8, weight=2)
    app.screens[6].rowconfigure(1, weight=1)
    app.screens[6].rowconfigure(8, weight=2)

    app.addScreen("Schiffsreisenplaner - Buchungen", (800,500))
    app.screens[7].items.append(CTkScrollableFrame(master=app.screens[7], label_text="Aktuelle Buchungen"))
    app.screens[7].items.append(CTkButton(app.screens[7], text="Zurück", command=lambda: app.switchScreen(4)))
    app.screens[7].items[0].grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[7].items[1].grid(row=1, column=1, columnspan=1, padx=10, pady=10, sticky=N+E+S+W)
    app.screens[7].columnconfigure(0, weight=1)
    app.screens[7].columnconfigure(2, weight=1)
    app.screens[7].rowconfigure(0, weight=1)
    app.screens[7].items[0].columnconfigure(0, weight=1)

    threading.Thread(target=loadingAll, args=(app,loadingVar)).start()
    app.start()
if __name__ == "__main__":
    files.loadSettings()
    main()