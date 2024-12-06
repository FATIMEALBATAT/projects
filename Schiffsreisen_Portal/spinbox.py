from customtkinter import *
import popup
from collections.abc import Callable

class Spinbox(CTkFrame):
    def __init__(self, *args,app, command: Callable = None, **kwargs):
        super().__init__(*args, **kwargs)

        self.step_size = 1
        self.command = command
        self.button_width = 40
        self.configure(fg_color="transparent")
        self.subtract_button = CTkButton(self, text="-",width=self.button_width,command=lambda: self.subtract_button_callback(app))
        self.subtract_button.grid(row=0, column=0, sticky=N+S+E+W)

        self.entry = CTkEntry(self, border_width=0, justify="center")
        self.entry.grid(row=0, column=1, padx=5,sticky=N+S+E+W)

        self.add_button = CTkButton(self, text="+", width=self.button_width,command=lambda: self.add_button_callback(app))
        self.add_button.grid(row=0, column=2)
        self.columnconfigure(1, weight=1)

        # default value
        self.entry.insert(0, "Beliebig")

    def add_button_callback(self, app):
        try:
            if self.entry.get() == "Beliebig":
                self.entry.delete(0, "end")
                self.entry.insert(0, 0)
            else:
                value = int(self.entry.get()) + self.step_size
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            popup.Popup("Geben sie bitte eine ganze Zahl!", app.returnCoords(popup.size))
        if self.command is not None:
            self.command()

    def subtract_button_callback(self, app):
        try:
            if self.entry.get() == "Beliebig":
                self.entry.delete(0, "end")
                self.entry.insert(0, 0)
            elif int(self.entry.get()) >= 0:
                value = int(self.entry.get()) - self.step_size
                self.entry.delete(0, "end")
                if value == -1:
                    self.entry.insert(0, "Beliebig")
                else:
                    self.entry.insert(0, value)
        except ValueError:
            popup.Popup("Geben sie bitte eine ganze Zahl!", app.returnCoords(popup.size))
        if self.command is not None:
            self.command()

    def get(self):
        try:
            if self.entry.get() == "Beliebig":
                return "Beliebig"
            else:
                return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))