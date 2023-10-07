import os
import tkinter as tk
from tkinter import ttk
import tkcalendar
from ttkthemes import ThemedTk
import datetime
#import db


def donothing():
   x = 0


class GUI:

    def __init__(self):
        # create root window object
        # themes listed here https://ttkthemes.readthedocs.io/en/latest/themes.html
        self.root = ThemedTk(theme="adapta")

        # create the tab system for the different categories of the app (clients, finances, appointments)
        self.tab_system = ttk.Notebook(self.root)

        # create tab objects
        self.tab_cli = Tab("Clients", self.root, self.tab_system, [
            TextField("Client Name"),
            TextField("Email"),
            TextField("Phone #"),
            TextField("Notes"),
        ])
        self.tab_fin = Tab("Finances", self.root, self.tab_system, [
            TextField("Transaction"),
            DateField("Date"),
            TextField("Time"),
            NumField("Earnings"),
            TextField("Notes"),
        ])
        self.tab_appt = Tab("Appointments", self.root, self.tab_system, [
            TextField("Client Name"),
            DateField("Date"),
            TextField("Time"),
            TextField("Notes"),
        ])
        self.tabs = [self.tab_cli, self.tab_fin, self.tab_appt]
        self.load_data()
        self.tab_system.pack(expand=True)

        self.root.mainloop()

    def load_data(self):
        for file in os.listdir("db"):
            if "cli.json" in file:
                print("Cli")
                #array = db.convert_to_json()s
            if "fin.json" in file:
                print("Fin")
            if "appt.json" in file:
                print("Appt")

    def save_data(self):
        pass


class Field:
    def __init__(self, field_name):
        self.field_name = field_name

    def create(self, frame):
        self.label = tk.Label(frame, text=self.field_name)

    def place(self, row):
        self.label.grid(column=0, row=row, padx=2, pady=2, sticky='w')


class TextField(Field):
    def __init__(self, field_name, width=25):
        super().__init__(field_name)
        self.width = width

    def create(self, frame):
        super().create(frame)
        self.field = ttk.Entry(frame, text=self.field_name, width=self.width)

    def place(self, row):
        super().place(row)
        self.field.grid(column=1, row=row, padx=2, pady=2, sticky='w')

    def value(self):
        return self.field.get()

    def update(self, value):
        self.field.delete(0, tk.END)
        self.field.insert(0, value)

    def default(self):
        return ''



class NumField(Field):
    def __init__(self, field_name, width=10):
        super().__init__(field_name)
        self.width = width

    def create(self, frame):
        super().create(frame)
        self.field = tk.Spinbox(frame, from_=-99999, to_=99999, increment=1, width=self.width)

    def place(self, row):
        super().place(row)
        self.field.grid(column=1, row=row, padx=2, pady=2, sticky='w')

    def value(self):
        return self.field.get()

    def update(self, value):
        self.field.delete(0, tk.END)
        self.field.insert(0, value)

    def default(self):
        return 0


class DateField(Field):
    def __init__(self, field_name):
        super().__init__(field_name)

    def create(self, frame):
        super().create(frame)
        self.field = tkcalendar.DateEntry(frame, width=16, foreground="white")

    def place(self, row):
        super().place(row)
        self.field.grid(column=1, row=row, padx=2, pady=2, sticky='w')

    def value(self):
        return self.field.get_date()

    def update(self, value):
        pass

    def default(self):
        return datetime.date.today()


class Tab:
    def __init__(self, name, root, tab_system, fields):
        self.root = root
        self.frame = ttk.Frame(tab_system)
        self.frame.grid_columnconfigure(0, weight=1)
        tab_system.add(self.frame, text=name)
        self.fields = fields

        # create frame to enter data into selected field
        self.field_frame = tk.Frame(self.frame)
        self.column_names = []
        row = 0
        for field in self.fields:
            field.create(self.field_frame) # add field field
            self.column_names.append(field.field_name)
            field.place(row)
            row += 1

        # Create a table object
        self.table = ttk.Treeview(self.frame, column=self.column_names, show='headings')

        col = 0
        for field in self.fields:
            col += 1
            self.table.heading("# " + str(col), text=field.field_name)

        self.table.pack()  # display the table

        add_row_button = tk.Button(self.frame, text="Add Entry", command=self.add_row)
        add_row_button.pack(fill=tk.X)
        submit_button = tk.Button(self.field_frame, text="Submit", command=self.submit_fields)
        submit_button.grid(sticky=tk.NSEW)

        # bring up field menu when a certain row of table is selected
        self.table.bind('<<TreeviewSelect>>', self.table_row_selected)
        # go to next field when enter is pressed
        self.root.bind('<Return>', lambda event: event.widget.tk_focusNext().focus_set())
        # press buttons when enter is pressed over them
        add_row_button.bind('<Return>', lambda event: self.add_row())
        submit_button.bind('<Return>', lambda event: self.submit_fields())

    def add_row(self):
        default_values = []
        for i in range(len(self.fields)):
            default_values.append(self.fields[i].default())
        new_row = self.table.insert('', 'end', values=default_values)
        self.table.selection_set(new_row)
        self.fields[0].field.focus_set()

    def table_row_selected(self, event):
        self.field_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        selected_row = self.table.selection()[0]
        print(self.table.item(selected_row)['values'])
        for i in range(len(self.fields)):
            value = self.table.item(selected_row)['values'][i]
            print(value)
            self.fields[i].update(value)
        self.fields[0].field.focus_set()

    def submit_fields(self):
        selected_row = self.table.selection()[0]
        submitted_values = []
        for field in self.fields:
            submitted_values.append(field.value())
        self.table.item(selected_row, text="", values=submitted_values)
        self.field_frame.pack_forget()
        self.get_dict()

    def get_dict(self):
        dict_array = []
        for x in self.table.get_children():
            value_dict = {}
            for col, item in zip(self.table["columns"], self.table.item(x)["values"]):
                value_dict[col] = item
            dict_array.append(value_dict)
        #print(dict_array)
        #json = db.convert_to_json(value_dict)
        #db.send_to_db(json)


GUI()