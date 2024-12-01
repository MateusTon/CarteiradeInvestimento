import customtkinter as ctk
from settings import *

class MenuTab(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(master=parent, bg_color=BG_COLOR, height=30)
        self.pack(expand=True, fill=ctk.X, padx=10)
        
        self.add('Carteira')
        self.add('Ordens')
        self.add('Procurar')