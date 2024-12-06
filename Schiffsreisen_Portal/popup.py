import customtkinter

size = (300, 100)

# Popup für Kleine Infos
class Popup(customtkinter.CTkToplevel):
    def __init__(self, text="", coords=(100, 100),*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("{}x{}".format(size[0], size[1])) # Fenstergröße
        self.geometry("+{}+{}".format(coords[0], coords[1])) # Position des Fensters
        self.title("Information")
        self.lift()
        self.attributes("-topmost", 4)
        self.label = customtkinter.CTkLabel(self, text=text)
        self.label.place(anchor="c",relx=0.5, rely=0.5)
        self.after(100, self.lift)