import tkinter as tk
import app
from tkinter import ttk,messagebox
import sqlite3
from create_dic import CreateDict

class ClientsPage(tk.Frame):
    def __init__(self, master, controller,window_size):
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
        #conect to database
        self.conection=sqlite3.Connection(self.dic_creator.dic.get("database"))
        self.db_cursor=self.conection.cursor()
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

        
        #entry points for Name, doc and telefono for new client
        tk.Label(self.top_frame,text="Nombre").pack(side=tk.LEFT,padx=5)
        self.name_entry=tk.Entry(self.top_frame)
        self.name_entry.pack(side=tk.LEFT,padx=5)
        tk.Label(self.top_frame,text="Cedula").pack(side=tk.LEFT,padx=5)
        self.doc_entry=tk.Entry(self.top_frame)
        self.doc_entry.pack(side=tk.LEFT,padx=5)
        tk.Label(self.top_frame,text="Telefono").pack(side=tk.LEFT,padx=5)
        self.phone_entry=tk.Entry(self.top_frame)
        self.phone_entry.pack(side=tk.LEFT,padx=5)
        
        #button for new client
        self.new_button=tk.Button(self.top_frame, text="Nuevo", 
                                    command=self.new_client)
        self.new_button.pack(side=tk.LEFT,padx=5,pady=5)

        #button to delete client
        self.delete_button=tk.Button(self.top_frame, text="Eliminar",command=self.delete_client)
        self.delete_button.pack(side=tk.LEFT,padx=5,pady=5)


    def set_table(self):
        columns=("ID","Nombre","Cedula","Telefono")
        #create the treeview widget
        self.treeview=ttk.Treeview(self.table_frame,columns=columns,
                                   show="headings",selectmode="browse")
        self.treeview.heading("ID",text="ID")
        self.treeview.heading("Nombre",text="Nombre")
        self.treeview.heading("Cedula",text="Cedula")
        self.treeview.heading("Telefono",text="Telefono")
        #set the columns widths
        self.treeview.column("ID",width=50)
        self.treeview.column("Nombre",width=150)
        self.treeview.column("Cedula",width=100)
        self.treeview.column("Telefono",width=100)
        #add treeview to the table_frame
        self.treeview.pack(fill="both",expand=True)
        #load data
        self.load_data()

    def load_data(self):
        #clean treeview data 
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        
        #fetch data
        self.db_cursor.execute("SELECT * FROM Clients")
        rows=self.db_cursor.fetchall()
        #insert data into
        for row in rows:
            self.treeview.insert("",tk.END,values=row)        

    def new_client(self):
        #get input
        name=self.name_entry.get().strip()
        doc=self.doc_entry.get().strip()
        phone=self.phone_entry.get().strip()
        #validate data input
        if not name or not doc or not phone:
            self.name_entry.delete(0,tk.END)
            self.doc_entry.delete(0,tk.END)
            self.phone_entry.delete(0,tk.END)
            messagebox.showerror("Error","Todos los campos son requeridos")
            return
        if not doc.isdigit():
            self.doc_entry.delete(0,tk.END)
            messagebox.showerror("Error","El documento debe ser un número")
            return
        if not phone.isdigit():
            self.phone_entry.delete(0,tk.END)
            messagebox.showerror("Error","El teléfono debe ser un número")
            return
        
        #check if client is already in database
        self.db_cursor.execute("SELECT * FROM Clients WHERE Cedula=?",(doc,))
        result=self.db_cursor.fetchone()
        if result:
            self.name_entry.delete(0,tk.END)
            self.doc_entry.delete(0,tk.END)
            self.phone_entry.delete(0,tk.END)
            messagebox.showwarning("Cliente duplicado",f"Cliente con cedula {doc} ya esta registrado")
        else:
            self.db_cursor.execute("INSERT INTO Clients (Nombre,Cedula,Telefono) VALUES(?, ?, ?)",(name,doc,phone))
            self.conection.commit()
            self.load_data()
            self.name_entry.delete(0,tk.END)
            self.doc_entry.delete(0,tk.END)
            self.phone_entry.delete(0,tk.END)
            messagebox.showinfo("Cliente agregado","Cliente agregado con exito")
    def delete_client(self):
        selected_item=self.treeview.focus()
        if not selected_item:
            messagebox.showerror("Error","Seleccione un cliente")
            return
        selected_client=self.treeview.item(selected_item,"values")
        doc=selected_client[2]
        #remove the client
        
        self.db_cursor.execute("DELETE FROM Clients WHERE Cedula=?",(doc,))
        self.conection.commit()
        self.treeview.delete(selected_item)
        messagebox.showinfo("Exito",f"Cliente con cedula {doc} eliminado exitosamente")
    def update_gui(self):
        pass