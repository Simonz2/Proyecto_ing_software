#Import libraries
import tkinter as tk
from app import App

#Create an instance of an application
def main():
    root=tk.Tk()#use tkinter as the main frame
    app=App(root)
    root.mainloop()

if __name__ =="__main__":#make sure this is run first
    main()