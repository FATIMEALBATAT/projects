from customtkinter import *
from PIL import ImageTk, Image
import screen

class Window(CTk):

    def __init__(self):
        super().__init__()
        self.title("Schiffsreisenplaner")
        self.resizable(False,False)
        self.wm_iconbitmap('assets/logo.ico')
        self.screens = []
        self.currentScreen = 0
        self.picWindow = None
        self.cityWindow = None
        self.bookingWindow = None
        self.results = []
        self.tempBuchungen = []
        self.lift()
        self.focus()
        self.attributes("-topmost", 1)
    def switchScreen(self,nr):
        if(len(self.screens) > nr and nr >= 0):
            self.geometry("{}x{}".format(self.screens[nr].size[0], self.screens[nr].size[1]))
            self.minsize(self.screens[nr].size[0], self.screens[nr].size[1])
            self.screens[self.currentScreen].forget()
            self.screens[nr].tkraise() # Hervorheben
            self.screens[nr].pack(anchor=N, fill=BOTH, expand=True)
            self.title(self.screens[nr].titel)
            self.resizable(self.screens[nr].resizeable,self.screens[nr].resizeable)
            self.currentScreen = nr; 
    def addScreen(self, titel, size=(0,0), resizeable=False):
        self.screens.append(screen.Screen(self))
        self.screens[len(self.screens)-1].setTitel(titel)
        self.screens[len(self.screens)-1].setSize(size,resizeable)
        if len(self.screens) > 0:
            self.screens[len(self.screens)-1].forget() # in den Hintergrund schieben
    def start(self):
        self.switchScreen(self.currentScreen)
        self.mainloop()
    def returnCoords(self, size=(100,100)):
        x = self.winfo_x() + (self.winfo_width() // 2) - (size[0] // 2)
        y = self.winfo_y() + (self.winfo_height() // 2) - (size[1] // 2)
        return (x, y)