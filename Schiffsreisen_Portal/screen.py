import tkinter as tk
from tkinter import ttk
from customtkinter import *

class Screen(CTkFrame): #https://stackoverflow.com/questions/12701206/how-to-extend-python-class-init
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, corner_radius=0)
        self.items = []
        self.titel = ""
        self.size = (0,0)
        self.resizeable = False
        self.pack(anchor=N, fill=BOTH, expand=True)
    def setTitel(self, titel = ""):
        self.titel = titel
    def setSize(self, size, resizeable):
        self.size = size
        self.resizeable = resizeable
