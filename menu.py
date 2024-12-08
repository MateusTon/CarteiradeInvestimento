import customtkinter as ctk
from stocks import *
from settings import *

class MenuTab(ctk.CTkTabview):
    def __init__(self, parent):
        super().__init__(master=parent, bg_color=BG_COLOR, anchor='nw', width=WINDOW_SIZE[0]-20, height=WINDOW_SIZE[1]-20)
        self.grid(padx=10, pady=10)
        
        self.add('Carteira')
        self.add('Ordens')
        self.add('Procurar')
        
        
        self.stocks = StocksSeacher(self.tab('Procurar'))
