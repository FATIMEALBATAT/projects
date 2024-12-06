from customtkinter import *

size = (500, 400)

# Popup für Kleine Infos
class PicPopup(CTkToplevel):
    def __init__(self, pics, curr: StringVar, coords=(100,100),*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("{}x{}".format(size[0], size[1])) # Fenstergröße
        self.geometry("+{}+{}".format(coords[0], coords[1])) # Position des Fensters
        self.title("Profilbild auswählen")
        self.resizable(False,False)
        self.attributes("-topmost", 3)
        self.items = []
        self.rows = 0
        self.columns = 0
        self.curr = curr
        self.scroll = CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.grid(row=0, column=0, columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        for i in pics:
            frame = CTkFrame(self.scroll)
            self.items.append(frame)
            pic = CTkLabel(frame, text="", image=CTkImage(light_image=pics[i], size=((100, 100))))
            radio = CTkRadioButton(frame,text=i,variable=curr,command=lambda: self.update() ,value=i,width=100)
            pic.grid(row=1, column=1,columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
            radio.grid(row=2, column=1,columnspan=1,padx=10, pady=10, sticky=N+E+S+W)
        for i in range(len(self.items)):
            if self.columns == 0:
                self.rows += 1
            self.items[i].grid(row=self.rows, column=self.columns, columnspan=1, padx=10, pady=10,sticky=N+E+S+W)
            self.columns = (self.columns + 1) % 3
        self.after(100, self.lift)
    def update(self):
        print("Update: " + self.curr.get())