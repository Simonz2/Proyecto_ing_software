#Import necessary libraries
import pandas as pd
import tkinter as tk
from tkinter import ttk
from create_dic import CreateDict
from create_table import CreateTable
import os
from editable_table import EditableTreeview



class BillingPage(tk.Frame):
    def __init__(self, master, controller, window_size, date=None, folder=None):
        # Initialize billing page frame
        super().__init__(master)
        
        # Store the controller and master window
        self.controller = controller
        self.root = master
        self.window_width = window_size[0]
        self.window_height = window_size[1]

        # Top Frame for buttons, bill title  and bill total
        self.start_position = (int(0.01 * self.window_width), int(0.01 * self.window_height))
        self.top_frame = tk.Frame(self, width=int(0.85 * self.window_width - 3 * self.start_position[0]),
                                  height=int(0.1 * self.window_height))
        self.top_frame.place(x=self.start_position[0], y=self.start_position[1],
                             width=int(0.85 * self.window_width - 3 * self.start_position[0]),
                             height=int(0.1 * self.window_height))
        self.set_buttons()

        # Store the date and folder path
        self.date = date
        self.folder_path = folder
        
        # Get the number of bills
        self.get_number_bills()

        # Get the bill title
        self.get_title()

        # Left Frame for scrollable selector
        self.left_frame = tk.Frame(self, width=int(self.window_width * 0.1),
                                   height=int(0.75 * self.window_height - 3 * self.start_position[1]))
        self.left_frame.place(x=self.start_position[0],
                              y=int(0.1 * self.window_height + 2 * self.start_position[1]),
                              width=int(self.window_width * 0.1),
                              height=int(0.75 * self.window_height - 3 * self.start_position[1]))
        self.selector_listbox = None
        self.selector_scrollbar = None
        self.selector_list()

        # Create table to show the bill
        self.set_table()

    def set_table(self,end_day=None):
        # Create a new frame for the table
        self.table_frame = tk.Frame(self, width=int(0.85 * self.window_width - 3 * self.start_position[0]),
                                    height=int(0.75 * self.window_height - 3 * self.start_position[1]))
        
        self.table_frame.place(x=int(0.1 * self.window_width + 2 * self.start_position[0]),
                               y=int(0.1 * self.window_height + 2 * self.start_position[0]),
                               width=int(0.85 * self.window_width - 3 * self.start_position[0]),
                               height=int(0.75 * self.window_height - 3 * self.start_position[1]))
        
        # Create a canvas and a scrollbar for the table
        self.canvas = tk.Canvas(self.table_frame,
                                width=int(0.85 * self.window_width - 3 * self.start_position[0]),
                                height=int(0.75 * self.window_height - 3 * self.start_position[1]))
        self.canvas.place(x=0, y=0, relheight=1, relwidth=1)
        self.scrollbar = ttk.Scrollbar(self.table_frame,
                                       orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Get the dataframe using the date
        self.df_creator = CreateTable()
        if end_day:
            self.df=self.df_creator.get_df(self.date, "Total_dia")
            if "Total_dia" not in self.selector_listbox.get(0,tk.END):
                self.selector_listbox.insert(tk.END, f"Total_dia")
        else:
            self.df = self.df_creator.get_df(self.date,self.title)

        df_columns = list(self.df.columns)

        # Create a new frame for the treeview widget
        self.tree = EditableTreeview(self.canvas,
                                     columns=df_columns,
                                     update_total_callback=self.update_total_on_edit,
                                     show="headings")
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Add the column headers
        for col in df_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=120, anchor="center")
        
        # Add rows to the table with alternating row colors
        for idx, row in self.df.iterrows():
            values = list(row)
            tag = 'oddrow' if idx % 2 else 'evenrow'
            self.tree.insert("", tk.END, values=values, tags=(tag,))
        
        # Define the tag configurations for alternating row colors
        self.tree.tag_configure('oddrow', background='white')
        self.tree.tag_configure('evenrow', background='lightgray')

        self.update_selector_list()
        self.set_total()
        

    def update_value_df(self):
        # Update the dataframe
        row_num = 0
        for row in self.tree.get_children():
            values = self.tree.item(row)['values']
            self.df.loc[int(row_num)] = [val if val is not None else "" for val in values]
            row_num += 1

    def set_buttons(self):
        # Function to set up the buttons
        self.get_back_button = ttk.Button(self.top_frame, text="Pagina Principal", command=self.controller.show_main_page)
        self.get_back_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.print_button = ttk.Button(self.top_frame, text="Imprimir factura", command=self.print_bill)
        self.print_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_bill_button = ttk.Button(self.top_frame, text="Guardar factura", command=self.save_bill)
        self.save_bill_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.new_bill_button = ttk.Button(self.top_frame, text="Nueva factura", command=self.new_bill)
        self.new_bill_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.end_day_button = ttk.Button(self.top_frame, text="Cerrar dia", command=self.end_day)
        self.end_day_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.bill_title_socket=ttk.Label(self.top_frame,text="")
        self.bill_title_socket.pack(side=tk.LEFT,padx=5,pady=5)
        
        self.bill_total_label=ttk.Label(self.top_frame,text="Total factura")
        self.bill_total_label.pack(side=tk.RIGHT,padx=5,pady=5)

        self.bill_total_p=ttk.Label(self.top_frame,text="0")
        self.bill_total_p.pack(side=tk.RIGHT,padx=5,pady=5)
        

    def selector_list(self):
        # Function for the selector list
        if self.selector_listbox:
            self.selector_listbox.destroy()
            self.selector_scrollbar.destroy()
        
        # Create selector box
        self.selector_listbox = tk.Listbox(self.left_frame,selectmode=tk.SINGLE)
        self.selector_listbox.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        
        # Add scrollbar to selector box
        self.selector_scrollbar = tk.Scrollbar(self.left_frame, orient="vertical", command=self.selector_listbox.yview)
        self.selector_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.selector_listbox.config(yscrollcommand=self.selector_scrollbar.set)
        
        # Add elements to the selector box
        for i in range(self.number_bills):
            self.selector_listbox.insert(tk.END, f"Factura_{i}")
        
        self.selector_listbox.bind("<<ListboxSelect>>", self.on_bill_select)

    def update_selector_list(self):
        new_item=f"Factura_{self.viewable_bill}"
        if new_item not in self.selector_listbox.get(0,tk.END):
            self.selector_listbox.insert(tk.END, f"Factura_{self.viewable_bill}")

    def on_bill_select(self, event):
        
        selected_index=self.selector_listbox.curselection()
        if selected_index:
            selected_item=str(self.selector_listbox.get(selected_index)).split("_")
            if selected_item[0]=="Total":
                selected_item="Total_dia"
                self.title=f"Total_dia"
                self.bill_path=self.folder_path+self.title                
                self.df = self.df_creator.get_df(self.date,self.title)
                self.set_table()
            else:
                self.viewable_bill=int(selected_item[1])
                self.get_title()
                self.df = self.df_creator.get_df(self.date,self.title)
                self.set_table()
        

    def get_title(self,end_day=None):
        if end_day:
            self.title = f"Total_dia"
        else:
            self.title = f"Factura_{self.viewable_bill}"
        
        if self.folder_path!=None:
            self.bill_path=self.folder_path+self.title

        else:
            self.bill_path=None
        
        #Set the bill title 
        if self.bill_title_socket:
            self.bill_title_socket.destroy()
        self.bill_title_socket=ttk.Label(self.top_frame,text=self.title)
        self.bill_title_socket.pack(side=tk.LEFT,padx=5,pady=5)

    def print_bill(self):
        self.save_bill()
        # Add printing functionality here

    def save_bill(self):
        self.update_value_df()
        self.df_creator.update_date(self.date,self.title)
        self.df_creator.update_df(self.df)
        self.df_creator.save_bill()
        self.update_selector_list()
        #print(self.title)

    def new_bill(self):
        self.save_bill()
        self.update_selector_list()
        self.viewable_bill = self.number_bills
        self.number_bills += 1
        self.get_title()
        self.update_selector_list()
        self.df = self.df_creator.get_df(self.date,self.title)
        self.set_table()
        self.df=self.df

    def get_number_bills(self):
        if not self.date:
            self.number_bills = 0
            self.viewable_bill = 0
        else:
            files = os.listdir(self.folder_path)
            f_path=os.path.join(self.folder_path,"Total_dia.csv")
        
            if os.path.exists(f_path):
                os.remove(os.path.abspath(f_path))

            numbers = sum(1 for f in files if os.path.isfile(os.path.join(self.folder_path, f)) 
                          and f.endswith(".csv") and f.startswith("Factura"))
            self.number_bills = numbers
            self.viewable_bill = numbers

    def set_total(self):
        self.update_value_df()
        self.total = 0
        x=self.df.get("Total")
        x=[float(y) if y else 0 for y in x]
        self.total = sum(x)
        self.bill_total_p.destroy()
        self.bill_total_p=ttk.Label(self.top_frame,text=str(self.total))
        self.bill_total_p.pack(side=tk.RIGHT,padx=5,pady=5)
    
    def update_total_on_edit(self):
        self.set_total()
        

    def end_day(self):
        self.save_bill()
        titles=self.selector_listbox.get(0,tk.END)
        self.df_creator.end_day_calc(titles)
        self.set_table(1)
        self.get_title(1)
        


    def update_gui(self):
        self.date = self.controller.date
        self.folder_path = self.controller.folder
        self.get_number_bills()
        self.get_title()
        self.selector_list()

    def update_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
