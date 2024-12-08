# Imports
import customtkinter as ctk
from settings import *
from menu import MenuTab
from stocks import *

class App(ctk.CTk): # Main class for the App
    def __init__(self):
        super().__init__(fg_color=BG_COLOR)
        self.geometry(f'{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}')
        self.title('Stocks')
        
        # Menu
        self.menu = MenuTab(self)
        self.bind('<Return>', self.menu.stocks.input_handler)
        
        self.mainloop()

App()