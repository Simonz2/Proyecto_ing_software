import tkinter as tk

class InsightsPage(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        
        tk.Button(self, text="Return to Main", command=controller.show_main_page).pack()