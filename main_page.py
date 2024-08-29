import tkinter as tk
from tkinter import ttk
from create_dic import CreateDict
from PIL import Image,ImageTk
from tkinter import filedialog
from paths_finder import PathsFinder
import os
import time


class MainPage(tk.Frame):
    def __init__(self, master,controller,window_size,date=None,folder=None):
        super().__init__(master)
        
        self.controller=controller
        self.root = master
        self.window_size=window_size
        self.date=date
        self.folder_selected=folder
        #Load and Set background image
        self.setup_background()

        # Create a frame for the buttons on the canvas
        self.setup_date()

        # This is crucial: pack or grid the MainPage frame itself into the master
        self.pack(fill=tk.BOTH, expand=True)  # Now, this should help in showing the frame
    
    def setup_date(self):
        #Create labels
        self.ylabel=tk.Label(self,text="Año")
        self.mlabel=tk.Label(self,text="Mes")
        self.dlabel=tk.Label(self,text="Dia")

        #Place labels on the canvas
        self.canvas.create_window(150,135,window=self.ylabel)
        self.canvas.create_window(250,135,window=self.mlabel)

        #Create entry zones
        self.yentry=tk.Entry(self,validate="key",justify="center")
        self.mentry=tk.Entry(self,validate="key",justify="center")
        self.dentry=tk.Entry(self,validate="key",justify="center")
        self.canvas.create_window(350,135,window=self.dlabel)

        #place entries on the canvas
        self.canvas.create_window(150,155,window=self.yentry,width=50)        
        self.canvas.create_window(250,155,window=self.mentry,width=50) 
        self.canvas.create_window(350,155,window=self.dentry,width=50)

        if self.date==None:
            #Create save date button
            self.save_date_button=tk.Button(self,text="Guardar",command=self.save_date)
            self.canvas.create_window(450,155,window=self.save_date_button)
        
        else:
            self.yentry.insert(0,self.date.split("-")[0])
            self.mentry.insert(0,self.date.split("-")[1])
            self.dentry.insert(0,self.date.split("-")[2])
            self.yentry.config(state="readonly")
            self.mentry.config(state="readonly")
            self.dentry.config(state="readonly")
            self.setup_buttons()

    def setup_background(self):
        dic_creator=CreateDict()
        bg_path=dic_creator.dic.get("background")
        image = Image.open(bg_path)  # Open the image file
        image = image.resize(self.window_size, Image.Resampling.LANCZOS)  # Resize image to fit the window
        self.bg_image = ImageTk.PhotoImage(image)  # Convert to PhotoImage
        
        #create canvas and put the background on it
        self.canvas=tk.Canvas(self,width=self.window_size[0],height=self.window_size[1])
        self.canvas.pack(fill=tk.BOTH,expand=True)
        self.canvas.create_image(0,0,image=self.bg_image,anchor="nw")
        
    def setup_buttons(self):
        #Create buttons and place them on the canvas
        self.billing_button=ttk.Button(self,text="Facturacion",command=self.billing_button_show)
        self.billing_button_window=self.canvas.create_window(120,450,anchor="nw",window=self.billing_button)
        

        self.business_insights_button=ttk.Button(self,text="Metricas de negocio",command=self.controller.show_insights_page)
        self.business_insights_button_window=self.canvas.create_window(265,450,anchor="nw",window=self.business_insights_button)

    def billing_button_show(self):
        while True: 
            try:  
                #if the folder hasn't been already selected
                if self.folder_selected is None:
                    #select the folder to save the bill of the day
                    self.folder_selected=filedialog.askdirectory()

                  

                    #check if the user pressed cancel
                    if not self.folder_selected:
                        raise Exception("No folder selected")
                
                    #is the folder path correct?
                    if os.path.isdir(self.folder_selected):
                        paths_finder=PathsFinder()
                        paths_finder.save_folder_path(self.date,self.folder_selected)
                        self.controller.folder=self.folder_selected
                        self.controller.show_billing_page()
                        break
                    else:#else call again the funtion to choose again the folder
                        print("Folder path is not correct")
                        raise Exception
                    
                else:
                    self.controller.show_billing_page()
                    break
            except Exception:
                self.show_error_msg("Por favor seleccione una carpeta adecuada")
                time.sleep(1)
                self.folder_selected=None
                
            
    
    def save_date(self):
        try:
            year=self.yentry.get()
            month=self.mentry.get()
            day=self.dentry.get()
            if not self.validate_year(year):
                self.error_msg="Año es numero entero y mayor a 2023"
                raise Exception
            if not self.validate_month(month):
                self.error_msg="Mes es numero entero entre 1 y 12"
                raise Exception
            if not self.validate_day(day):
                self.error_msg="Dia es un numero entero entre 1 y 31"
                raise Exception
            
            self.date="".join([year,"-",month,"-",day])
            self.controller.date=self.date
            self.save_date_button.destroy()
            self.yentry.config(state="readonly")
            self.mentry.config(state="readonly")
            self.dentry.config(state="readonly")
            self.setup_buttons()
        except Exception:
            self.show_error_msg(self.error_msg)
        
        
    def validate_year(self,P):
        if P.isdigit() and int(P)>2023:
            return True
        else:
            self.yentry.delete(0,tk.END)
            return False
    def validate_month(self,P):
        if P.isdigit() and 1<=int(P)<=12:
            return True
        else:
            self.mentry.delete(0,tk.END)
            return False
    def validate_day(self,P):
        if P.isdigit() and 1<=int(P) and int(P)<=31:
            return True
        else:
            self.dentry.delete(0,tk.END)
            return False
    
    def show_error_msg(self,msg):
        error_popup=tk.Toplevel()
        error_popup.title("Error")
        error_popup.geometry("300x100")
        label=tk.Label(error_popup,text=msg,wraplength=250)
        label.pack(expand=True,padx=10,pady=10)
        error_popup.after(3000,error_popup.destroy)
