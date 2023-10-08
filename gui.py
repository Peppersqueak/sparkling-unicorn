import os
import random
import tkinter as tk
from tkinter import ttk
import tkcalendar
from tkinter import messagebox
from ttkthemes import ThemedTk
import datetime
import local_pipe


def donothing():
   x = 0


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


class GUI:

    def __init__(self):
        # create root window object
        # themes listed here https://ttkthemes.readthedocs.io/en/latest/themes.html
        self.root = tk.Tk()#ThemedTk(theme="adapta")
        self.root.title("Omnibalance")

        # create the tab system for the different categories of the app (clients, finances, appointments)
        self.tab_system = ttk.Notebook(self.root)

        # create tab objects
        self.tab_cli = Tab("Clients", "cli", self.root, self.tab_system, [
            TextField("Last Name"),
            TextField("First Name"),
            TextField("Email"),
            TextField("Phone #"),
            TextField("Notes"),
        ])
        self.tab_fin = Tab("Financial", "fin", self.root, self.tab_system, [
            TextField("Transaction"),
            DateField("Date"),
            TextField("Time"),
            NumField("Earnings ($)"),
            TextField("Notes"),
        ])
        self.tab_appt = Tab("Appointments", "appt", self.root, self.tab_system, [
            TextField("Client Name"),
            DateField("Date"),
            TextField("Time"),
            TextField("Notes"),
        ])

        self.load_data()
        self.tab_system.pack(expand=True)

        #self.timeline = ttk.Frame(self.tab_system)
        #self.timeline.grid_columnconfigure(0, weight=1)
        #self.tab_system.add(self.timeline, text="Timeline")
        #self.tab_system.bind('<<NotebookTabChanged>>', self.refresh_timeline)
        #self.tab_appt.submit_button.bind('<<NotebookTabChanged>>', self.refresh_timeline)

        self.root.mainloop()  # run the program

    """
    def refresh_timeline(self, event):
        m = 0
        for widget in self.timeline.winfo_children():
            widget.destroy()
        for appt in self.tab_appt.create_dicts():

            l1 = tk.Label(self.timeline, text=appt["Client Name"])
            l2 = tk.Label(self.timeline, text=appt["Date"])
            l3 = tk.Label(self.timeline, text=appt["Time"])
            l4 = tk.Label(self.timeline, text=appt["Notes"])
            l1.grid(column=0, row=m, sticky='nsew')
            l2.grid(column=1, row=m, sticky='nsew')
            l3.grid(column=2, row=m, sticky='nsew')
            l4.grid(column=3, row=m, sticky='nsew')
            m += 1
    """

    def load_data(self):
        for file_name in os.listdir("db"):
            tab_to_load = None
            if "cli.json" in file_name:  # if part of name matches
                print("cli file found")
                tab_to_load = self.tab_cli
            if "fin.json" in file_name:
                print("cli file found")
                tab_to_load = self.tab_fin
            if "appt.json" in file_name:
                print("appt file found")
                tab_to_load = self.tab_appt

            if tab_to_load is not None:
                array = local_pipe.FromDatabase(tab_to_load.file_name).grab_from_DB()
                if array is not None:
                    for row in array:
                        tab_to_load.add_row()

                        field_names = []
                        for field in tab_to_load.fields:
                            field_names.append(field.field_name)
                        k = 0

                        try:
                            for name in field_names:
                                tab_to_load.fields[k].update(row[name])
                                tab_to_load.submit_fields()
                                k += 1
                        except:
                            print("unable to read " + tab_to_load.file_name)


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
        super().update(value)

    def default(self):
        return datetime.date.today()


class TimeField(TextField):
    def __init__(self, field_name):
        super().__init__(field_name)

    def create(self, frame):
        super().create(frame)

    def place(self, row):
        super().place(row)

    def value(self):
        return datetime.datetime.strptime(self.field.get(), "%H:%M %p")

    def update(self, value):
        super().update(value)

    def default(self):
        return datetime.datetime.now().strftime("%H:%M %p")


class Tab:
    def __init__(self, category, file_name, root, tab_system, fields):
        self.category = category
        self.file_name = file_name
        self.root = root
        self.frame = ttk.Frame(tab_system)
        self.frame.grid_columnconfigure(0, weight=1)
        tab_system.add(self.frame, text=category)

        self.fields = fields
        # create frame to enter data into selected field
        self.field_frame = tk.Frame(self.frame)
        self.column_names = []
        row = 0
        for field in self.fields:
            field.create(self.field_frame)
            self.column_names.append(field.field_name)
            field.place(row)
            row += 1

        # Create a table object
        self.table = ttk.Treeview(self.frame, column=self.column_names, show='headings')

        col = 0
        for field in self.fields:
            print("COLS   " + str(col) + "   " + str(len(self.table.get_children())))
            self.table.heading(field.field_name, text=field.field_name, command=lambda: treeview_sort_column(self.table, 0, False))
            col += 1

        self.table.pack()  # display the table

        action_frame = tk.Frame(self.frame)
        add_row_button = tk.Button(action_frame, text="Add Entry", command=self.add_row)
        add_row_button.grid(row=0, column=0, sticky='nsew')
        remove_row_button = tk.Button(action_frame, text="Remove Entry", command=self.remove_selected_row)
        remove_row_button.grid(row=0, column=1, sticky='nsew')
        action_frame.pack(expand=True, fill=tk.X, anchor=tk.S)

        self.submit_button = tk.Button(self.field_frame, text="Update Entry", command=self.submit_fields)
        self.submit_button.grid(column=1, sticky=tk.NSEW)

        # bring up field menu when a certain row of table is selected
        self.table.bind('<<TreeviewSelect>>', self.table_row_selected)
        # go to next field when enter is pressed
        self.root.bind('<Return>', lambda event: event.widget.tk_focusNext().focus_set())
        # press buttons when enter is pressed over them
        add_row_button.bind('<Return>', lambda event: self.add_row())
        self.submit_button.bind('<Return>', lambda event: self.submit_fields())

    def add_row(self):
        default_values = []
        for i in range(len(self.fields)):
            default_values.append(self.fields[i].default())
        new_row = self.table.insert('', 'end', values=default_values)
        self.table.selection_set(new_row)
        self.fields[0].field.focus_set()

    def remove_selected_row(self):
        if messagebox.askyesno("Confirm removal", "Are you sure?"):
            try:
                self.table.delete(self.table.selection()[0])
                self.save_to_file()
            except:
                pass
        self.table.selection_clear()
        self.field_frame.grid_forget()  # not unfocusing

    def table_row_selected(self, event):
        self.field_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        try:
            selected_row = self.table.selection()[0]
            for i in range(len(self.fields)):
                value = self.table.item(selected_row)['values'][i]
                #print(value)
                self.fields[i].update(value)
        except:
            pass
        self.fields[0].field.focus_set()

    def submit_fields(self):
        selected_row = self.table.selection()[0]
        submitted_values = []
        for field in self.fields:
            submitted_values.append(field.value())
        self.table.item(selected_row, text="", values=submitted_values)
        self.field_frame.pack_forget()
        self.save_to_file()

    def create_dicts(self):
        dicts = []
        for x in self.table.get_children():
            print("dicts:   " + str(x))
            value_dict = {}
            for col, item in zip(self.table["columns"], self.table.item(x)["values"]):
                value_dict[col] = item
            dicts.append(value_dict)
        return dicts

    def save_to_file(self):
        dicts = []
        for x in self.table.get_children():
            print("dicts:   " + str(x))
            value_dict = {}
            for col, item in zip(self.table["columns"], self.table.item(x)["values"]):
                value_dict[col] = item
            dicts.append(value_dict)
        save = local_pipe.ToDatabase(self.file_name).convert_to_json(dicts)


GUI()