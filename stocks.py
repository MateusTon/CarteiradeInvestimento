from settings import *
import customtkinter as ctk
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class StocksSeacher(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master= parent, bg_color=BG_COLOR, 
                         width=WINDOW_SIZE[0] - 20, height=WINDOW_SIZE[1]-20,
                         corner_radius= 10)
        self.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Data
        self.input_string = ctk.StringVar(value= 'HGLG11.SA')
        self.time_string = ctk.StringVar(value= TIME_OPTIONS[0])
        self.time_string.trace_add('write', self.create_graph)
        self.has_data = False
        
        # Widgets
        self.graph_panel = None
        InputPanel(self, self.input_string, self.time_string)      

        
    def create_graph(self, *args):
        if self.graph_panel: self.graph_panel.pack_forget()
        if self.has_data:
            match self.time_string.get():
                case 'Max': data = self.max
                case '1 Year': data = self.year
                case '6 Months': data = self.six_months
                case 'Month': data = self.one_month
                case 'Week': data = self.one_week
                case _:  # Caso padrão para valores inesperados
                    return
            self.graph_panel = GraphPanel(self, data)
        
        
    def input_handler(self, event=None):
        ticker = yf.Ticker(self.input_string.get())
        start = datetime(1950,1,1)
        end = datetime.today()
        
        self.max = ticker.history(start= start, end= end, period= '1d')
        self.year = self.max.iloc[-260:]
        self.six_months = self.max.iloc[-130:]
        self.one_month = self.max.iloc[-21:]
        self.one_week = self.max.iloc[-5:]
        self.has_data = True
        
        self.create_graph()
    

class InputPanel(ctk.CTkFrame): # Class for the bottom panel
    def __init__(self, parent, input_string, time_string):
        super().__init__(master= parent, fg_color=BG_COLOR, corner_radius=10)
        self.pack(fill='both', side='bottom')
        
        # Widgets
        ctk.CTkEntry(self, textvariable=input_string, fg_color=BG_COLOR, border_color=TEXT_COLOR, border_width=1).pack(side='left', padx=10, pady=10)
        self.buttons = [TextButton(self, option, time_string) for option in TIME_OPTIONS]
        
        # If one button has been clicked, calls the unselect all buttons function
        time_string.trace('w', self.unselect_all_buttons)
        
    # Calls the function that turns the buttons into white for every button
    def unselect_all_buttons(self, *args):
        for button in self.buttons:
            button.unselect()

# Widgets for the frames:
class TextButton(ctk.CTkLabel): # Class for the buttons in the Bottom Panel
    def __init__(self, parent, text, time_string):
        super().__init__(master= parent, text=text, fg_color=BG_COLOR)
        self.pack(side='right', padx=10, pady=10)    
        self.bind('<Button>', self.select_handler)
        
        self.time_string = time_string
        self.text= text
        
        # Set Max option as default
        if time_string.get() == text:
            self.select_handler()
        
    # Function thats highlights de buttons clicked
    def select_handler(self, event=None):
        self.time_string.set(self.text)
        self.configure(text_color=HIGHLIGHT_COLOR)
        
    # Function called to turn the buttons white again
    def unselect(self):
        self.configure(text_color=TEXT_COLOR)
   
class GraphPanel(ctk.CTkFrame): # Class for the stock graph 
    def __init__(self, parent, data):
        super().__init__(master=parent, fg_color=BG_COLOR, corner_radius=10)
        self.pack(expand=True, fill='both', pady=(0,10))
        
        # Figure
        figure = plt.Figure()
        figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
        #figure.patch.set_facecolor(BG_COLOR)        
        figure.patch.set_alpha(0)
    
        # Graph
        ax = figure.add_subplot(111)
        ax.set_facecolor(BG_COLOR)
        for side in ['top', 'left', 'right', 'bottom']:
            ax.spines[side].set_color(BG_COLOR)
            
        line = ax.plot(data['Close'])[0]
        line.set_color(HIGHLIGHT_COLOR)
        
        # Ticks
        ax.tick_params(axis='x', direction='in', pad=-14, colors=TICK_COLOR)
        ax.yaxis.tick_right()
        ax.tick_params(axis='y', direction='in', pad=-22 , colors=TICK_COLOR)
        
        # Widget
        figure_widget = FigureCanvasTkAgg(figure, master=self)
        figure_widget.get_tk_widget().pack(side=ctk.TOP, fill='both', expand=True)
        