from tkinter import ttk
import tkinter as tk


class EditableTreeview(ttk.Treeview):
    def __init__(self, master=None, update_total_callback=None,**kw):
        super().__init__(master, **kw)
        self.update_total_callback=update_total_callback
        self.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        region = self.identify("region", event.x, event.y)
        if region == "cell":
            row_id = self.identify_row(event.y)
            column = self.identify_column(event.x)
            if column == "#3":  # Only the third column should be editable
                self.edit_cell(row_id, column)

    def edit_cell(self, row_id, column):
        x, y, width, height = self.bbox(row_id, column)
        value = self.item(row_id, "values")[int(column[1:])-1]
        entry = tk.Entry(self)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, value)
        entry.focus()

        def save_edit(event):
            new_value = entry.get()
            col_idx = int(column[1:]) - 1
            current_values = list(self.item(row_id, "values"))
            current_values[col_idx] = new_value

            # Update the fourth column with the multiplication of the second and third columns
            try:
                
                second_col_value = float(current_values[1])
                third_col_value = float(new_value)
                current_values[3] = str(second_col_value * third_col_value)
            except ValueError:
                current_values[2]=""
                current_values[3] =""

            self.item(row_id, values=current_values)
            entry.destroy()

            if self.update_total_callback:
                self.update_total_callback()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda event: entry.destroy())

