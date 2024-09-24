#Import necessary librarieslibraries
import tkinter as tk
from billing_page import BillingPage
from main_page import MainPage
from insights_page import InsightsPage
from clients_page import ClientsPage
from menu_page import MenuPage

class App:
    def __init__(self,master):
        #Initialize the application with a master window
        self.master=master
        self.master.title("Sabor y Arte al carbon")
        #set the title of the window
        
        # Calculate position to center the window
        self.screen_width=self.master.winfo_screenwidth()
        self.screen_height=self.master.winfo_screenheight()
        self.x_position = int((self.screen_width - self.screen_width) / 2)
        self.y_position = int((self.screen_height - self.screen_height) / 2)
        
        #Set the window size
        self.window_size=(500,600)
        self.master.geometry(f"{self.window_size[0]}x{self.window_size[1]}")
        self.master.resizable(False,False)#make the window non-resizable
        
        #Initialize variable to store the folder and date
        self.folder=None
        self.date=None

        #Create instances of main page, billing page and insights page
        self.main_page=MainPage(self.master,self,self.window_size,self.date,self.folder)
        self.billing_page=BillingPage(self.master,self,(self.screen_width,self.screen_height),self.date,self.folder)
        self.insights_page=InsightsPage(self.master,self)
        self.clients_page=ClientsPage(self.master,self,(self.screen_width,self.screen_height))
        self.menu_page=MenuPage(self.master,self,(self.screen_width,self.screen_height))

        #Show the main page initially
        self.show_main_page()

    def show_main_page(self):
        #Hide billing page and insights page and menu page
        self.billing_page.pack_forget()
        self.insights_page.pack_forget()
        self.clients_page.pack_forget()
        self.menu_page.pack_forget()
        #Set the window size back toç original size
        self.master.geometry(f"{self.window_size[0]}x{self.window_size[1]}")
        #Show main page
        self.main_page.pack(fill="both",expand=True)

    def show_billing_page(self):
        #Hide main page, insights page and client page and menu page
        self.main_page.pack_forget()
        self.insights_page.pack_forget()
        self.clients_page.pack_forget()
        self.menu_page.pack_forget()
        #Update the date and folder variable from the main page 
        self.date=self.main_page.date
        self.folder=self.main_page.folder_selected
        #Update the GUI of the billig page
        self.billing_page.update_gui()
        # Set geometry to full screen but keep window frame centered
        self.master.geometry(f"{self.screen_width}x{self.screen_height-40}+0+0")
        self.billing_page.pack(fill="both",expand=True)
        #Show billing page
        self.billing_page.update_gui()
        
    def show_insights_page(self):
        #Hide main page, billing page and client page and menu page
        self.billing_page.pack_forget()
        self.insights_page.pack_forget()
        self.clients_page.pack_forget()
        self.menu_page.pack_forget()
        # Set geometry to full screen and keep window frame, centered
        self.master.geometry(f"{self.window_size[0]}x{self.window_size[1]}")
        self.main_page.pack(fill="both",expand=True)
    
    def show_clients_page(self):
        #Hide main page and billing page and insights page and menu page
        self.billing_page.pack_forget()
        self.insights_page.pack_forget()
        self.main_page.pack_forget()
        self.menu_page.pack_forget()
        # Set geometry to full screen but keep window frame centered
        self.master.geometry(f"{self.screen_width}x{self.screen_height-40}+0+0")
        #Show clients page
        self.clients_page.pack(fill="both",expand=True)

    def show_menu_page(self):
        #Hide main page and billing page and insights page and clients page
        self.billing_page.pack_forget()
        self.insights_page.pack_forget()
        self.main_page.pack_forget()
        self.clients_page.pack_forget()
        # Set geometry to full screen but keep window frame centered
        self.master.geometry(f"{self.screen_width}x{self.screen_height-40}+0+0")
        #Show clients page
        self.menu_page.pack(fill="both",expand=True)