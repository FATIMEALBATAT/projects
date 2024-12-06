from customtkinter import *

size = (500, 500)

# Popup für Kleine Infos
class InfoPopup(CTkToplevel):
    def __init__(self, text="", curr=None, data=[], coords=(100,100),*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("{}x{}".format(size[0], size[1])) # Fenstergröße
        self.geometry("+{}+{}".format(coords[0], coords[1])) # Position des Fensters
        self.title("Information")
        self.resizable(False,False)
        self.attributes("-topmost", 3)
        self.items = []
        self.info = CTkLabel(self, text=text)
        self.info.grid(row=0, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        if type(curr) is str:
            self.curr = CTkLabel(self, text="Aktuelle Auswahl: {}".format(curr))
            self.curr.grid(row=2, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        elif type(curr) is list:
            staedtestr = ""
            for j in range(len(curr)):
                if j % 4 == 0 and j > 0:
                    staedtestr += "\n"
                staedtestr += curr[j]
                if j + 1 < len(curr):
                    staedtestr += ", "
            self.curr = CTkLabel(self, text="Aktuelle Auswahl: \n{}".format(staedtestr))
            self.curr.grid(row=2, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.columnconfigure(0, weight=1)
        if len(data) > 0:
            self.rowconfigure(1, weight=1)
            self.scroll = CTkScrollableFrame(self, fg_color="transparent")
            self.scroll.grid(row=1, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
            self.scroll.columnconfigure(0, weight=1)
            for i in range(len(data)):
                frame = CTkFrame(self.scroll)
                self.items.append(frame)
                text = CTkLabel(frame, text=data[i]["text"])
                if "pic" in data[i] and data[i]["pic"] != None:
                    pic = CTkLabel(frame, text="", image=CTkImage(light_image=data[i]["pic"], size=((400, 300))))
                    pic.grid(row=0, column=0,columnspan=1,padx=10, pady=(10,0), sticky=N+E+S+W)
                    text.grid(row=1, column=0,columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
                else:
                    text.grid(row=0, column=0,columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
            for i in range(len(self.items)):
                self.items[i].grid(row=i, column=0, columnspan=1, padx=10, pady=10,sticky=N+E+S+W)
        else:
            self.rowconfigure(0, weight=1)
            self.geometry("{}x{}".format(400, 200)) # Fenstergröße
        self.after(100, self.lift)
    def setSize(self, size):
        self.geometry("{}x{}".format(size[0], size[1]))