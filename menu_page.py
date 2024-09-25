import app
import tkinter as tk
from tkinter import ttk, messagebox
from create_dic import CreateDict
import pandas as pd
import os

class MenuPage(tk.Frame):
    def __init__(self,master,controller,window_size):
                #initialize client page frame
        super().__init__(master)
        #stor controller and master window
        self.root=master
        self.controller:app.App=controller
        #get window size
        self.window_width=window_size[0]
        self.window_height=window_size[1]
        #get dic for paths
        self.dic_creator:CreateDict=CreateDict()
        #create top frame for buttons and
        #  bottom frame for the clients treeview
        self.start_position = (int(0.01 * self.window_width), 
                               int(0.01 * self.window_height))
        self.top_frame = tk.Frame(self, width=int(0.98 * self.window_width - 3 * self.start_position[0]),
                                  height=int(0.1 * self.window_height))
        self.top_frame.place(x=self.start_position[0], y=self.start_position[1],
                             width=int(0.98 * self.window_width - 3 * self.start_position[0]),
                             height=int(0.1 * self.window_height))
        
        self.table_frame = tk.Frame(self, width=int(0.98 * self.window_width - 3 * self.start_position[0]),
                                    height=int(0.75 * self.window_height - 3 * self.start_position[1]))
        
        self.table_frame.place(x=self.start_position[0],
                               y=int(0.1 * self.window_height + 2 * self.start_position[0]),
                               width=int(0.98 * self.window_width - 3 * self.start_position[0]),
                               height=int(0.75 * self.window_height - 3 * self.start_position[1]))
        self.set_buttons()
        self.set_table()

    def show_billing_page_t(self):
        if self.controller.folder is None:
              self.controller.show_main_page()
        else:
             self.controller.show_billing_page()

    def set_buttons(self):
        #crate buttons:back, bill, new client, and several labels(name,cedula)
        self.back_button=tk.Button(self.top_frame, text="Pantalla principal", 
                                    command=self.controller.show_main_page)
        self.back_button.pack(side=tk.LEFT,padx=5,pady=5)
        self.bill_button=tk.Button(self.top_frame, text="Facturacion",
                                    command=self.show_billing_page_t)
        self.bill_button.pack(side=tk.LEFT,padx=5,pady=5)
        #entry points for Product
        tk.Label(self.top_frame,text="Producto").pack(side=tk.LEFT,padx=5)
        self.name_entry=tk.Entry(self.top_frame)
        self.name_entry.pack(side=tk.LEFT,padx=5)
        tk.Label(self.top_frame,text="Precio").pack(side=tk.LEFT,padx=5)
        self.price_entry=tk.Entry(self.top_frame)
        self.price_entry.pack(side=tk.LEFT,padx=5)

        #button for new product
        self.new_button=tk.Button(self.top_frame, text="Nuevo", 
                                    command=self.new_product)
        self.new_button.pack(side=tk.LEFT,padx=5,pady=5)
        self.delete_button=tk.Button(self.top_frame, text="Eliminar",
                                     command=self.delete_product)
        self.delete_button.pack(side=tk.LEFT,padx=5,pady=5)

    def set_table(self):
        columns=("Producto","Precio")
        #create the treeview widget
        self.treeview=ttk.Treeview(self.table_frame,columns=columns,
                                   show="headings",selectmode="browse")
        self.treeview.heading("Producto",text="Producto")
        self.treeview.heading("Precio",text="Precio")

        #set the columns widths
        self.treeview.column("Producto",width=200)
        self.treeview.column("Precio",width=150)
        
        #add treeview to the table_frame
        self.treeview.pack(fill="both",expand=True)
        #load data
        self.load_data()

    def load_data(self):
        #clear the treeview
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        #load data
        self.Productos_path=self.dic_creator.dic.get("Productos")
        self.df=pd.read_csv(self.Productos_path,sep=";")
        self.df.dropna(axis=1,how="all",inplace=True)
        
        #insert data into treeview
        for idx, row in self.df.iterrows():
            values = list(row)
            self.treeview.insert("", tk.END, values=values)

    def new_product(self):
        product=self.name_entry.get().strip()
        price=self.price_entry.get().strip()
        if not product or not price:
            self.name_entry.delete(0,tk.END)
            self.price_entry.delete(0,tk.END)
            messagebox.showerror("Error","Rellenar nombre de producto y precio")
            return
        if not price.isdigit():
            messagebox.showerror("Error","Precio debe ser un numero")
            return
        
        price=int(price)
        if product in self.df["PDTO"].values:
            self.df.loc[self.df["PDTO"]==product,"VALOR"]=price
            messagebox.showinfo("Actualizado",f"Precio de producto {product} fue actualizado")
        else:
            self.df.loc[len(self.df.index)]=[product,price]
            messagebox.showinfo("Agregado",f"Producto: {product} fue agregado")
        
        self.name_entry.delete(0,tk.END)  
        self.price_entry.delete(0,tk.END)
        
        self.save_edit()
        self.load_data()

    def delete_product(self):
        selected_item=self.treeview.focus()
        if not selected_item:
            messagebox.showerror("Error","Seleccionar un producto")
            return
        selected_product=self.treeview.item(selected_item,"values")
        #print(selected_product)

        self.df.drop(self.df[self.df["PDTO"]==selected_product[0]].index,inplace=True)

        self.treeview.delete(selected_item)
        self.save_edit()

    def save_edit(self):#save the new products into the csv
        if os.path.isfile(self.Productos_path):
            os.remove(self.Productos_path)
        self.df.to_csv(self.Productos_path,sep=";",index=False)