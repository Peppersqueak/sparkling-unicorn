import tkinter as tk
from tkinter import ttk
import tkcalendar
from ttkthemes import ThemedTk
import datetime
#import client;


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
            TextEntry("Client Name"),
            DateEntry("Date"),
            TimeEntry("Time")
        ])
        self.tab_fin = Tab("Finances", self.root, self.tab_system, [
            TextEntry("Transaction"),
            DateEntry("Date"),
            TimeEntry("Time"),
            NumEntry("Money", 10),
        ])

        #self.tab_system.add(self.tab_cli.frame, text='Clients')
        #self.tab_system.add(self.tab_fin.frame, text='Finances')
        self.tab_system.pack(expand=True)

        self.root.mainloop()


# FIELD TYPES
FIELD_TEXT = 0
FIELD_DATE = 1
FIELD_TIME = 2
FIELD_NUM = 3


class Entry:
    def __init__(self, field_name):
        self.field_name = field_name

    def create(self, frame):
        self.label = tk.Label(frame, text=self.field_name)


class TextEntry(Entry):
    def __init__(self, field_name):
        super().__init__(field_name)

    def create(self, frame):
        super().create(frame)
        self.entry = ttk.Entry(frame, text=self.field_name)

    def place(self, row):
        self.label.grid(column=0, row=row, padx=2, pady=2, sticky='w')
        self.entry.grid(column=1, row=row, padx=2, pady=2, sticky='w')



class NumEntry(Entry):
    def __init__(self, field_name, width):
        super().__init__(field_name)
        self.width = width

    def create(self, frame):
        super().create(frame)
        self.entry = tk.Spinbox(frame, from_=-99999, to_=99999, increment=1, width=self.width)

    def place(self, row):
        self.label.grid(column=0, row=row, padx=2, pady=2, sticky='w')
        self.entry.grid(column=1, row=row, padx=2, pady=2, sticky='w')


class DateEntry(Entry):
    def __init__(self, field_name):
        super().__init__(field_name)

    def create(self, frame):
        super().create(frame)
        self.entry = tkcalendar.DateEntry(frame, width=16, foreground="white", bd=2)

    def place(self, row):
        self.label.grid(column=0, row=row, padx=2, pady=2, sticky='w')
        self.entry.grid(column=1, row=row, padx=2, pady=2, sticky='w')


class TimeEntry(Entry):
    def __init__(self, field_name):
        super().__init__(field_name)

    def create(self, frame):
        super().create(frame)
        self.subframe = tk.Frame(frame)
        self.hour_entry = tk.Spinbox(self.subframe, from_=1, to_=12, increment=1, wrap=True, width=3)
        self.colon = tk.Label(self.subframe, text=":")
        self.min_entry = tk.Spinbox(self.subframe, from_=0, to_=59, increment=1, wrap=True, width=3)

    def place(self, row):
        self.label.grid(column=0, row=row, padx=2, pady=2, sticky='w')
        self.hour_entry.grid(column=1, row=row, padx=2, pady=2, sticky='w')
        self.colon.grid(column=2, row=row, padx=2, pady=2, sticky='w')
        self.min_entry.grid(column=3, row=row, padx=2, pady=2, sticky='w')
        self.subframe.grid(column=1, row=row, columnspan=1, sticky='w')



class Tab:
    def __init__(self, name, root, tab_system, fields):
        self.root = root
        self.frame = ttk.Frame(tab_system)
        self.frame.grid_columnconfigure(0, weight=1)
        tab_system.add(self.frame, text=name)
        self.fields = fields

        # create frame to enter data into selected field
        self.entry_frame = tk.Frame(self.frame)
        self.column_names = []
        row = 0
        for field in self.fields:
            field.create(self.entry_frame) # add field entry
            self.column_names.append(field.field_name)
            field.place(row)
            row += 1

        # Create a table object
        self.table = ttk.Treeview(self.frame, column=self.column_names, show='headings')

        col = 0
        for field in self.fields:
            col += 1
            #self.table.column("# " + str(col))
            self.table.heading("# " + str(col), text=field.field_name)

        # Insert the data into the table
        self.table.insert('', 'end', text="1", values=('Amit',
                                                       datetime.date(year=2004, month=12, day=2),
                                                       datetime.time(hour=2,minute=30).strftime("%I:%M %p")))
        self.table.insert('', 'end', text="1", values=('Ankush',
                                                       datetime.date(year=2004, month=12, day=2),
                                                       datetime.time(hour=2,minute=30).strftime("%I:%M %p")))
        self.table.insert('', 'end', text="1", values=('Manisha',
                                                       datetime.date(year=2004, month=12, day=2),
                                                       datetime.time(hour=14,minute=30).strftime("%I:%M %p")))
        self.table.insert('', 'end', text="1", values=('Manisha2',
                                                       datetime.date(year=2004, month=12, day=2),
                                                       datetime.time(hour=14,minute=30).strftime("%I:%M %p")))

        self.table.pack()  # display the table

        # bring up entry menu when a certain row of table is selected
        self.table.bind('<<TreeviewSelect>>', lambda selected: self.table_row_selected())


        add_row_button = tk.Button(self.frame, text="Add Row", command=self.add_row)
        add_row_button.pack(fill=tk.X)

        submit_entry_button = tk.Button(self.entry_frame, text="Submit", command=self.submit_entry)
        submit_entry_button.grid(column=3, row=0, rowspan=3, sticky=tk.NSEW)

    def table_row_selected(self):
        self.entry_frame.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)
        print("hi")

    def add_row(self):
        print("Add row")
        self.table.insert('', 'end', values=('Manisha',
                                                       datetime.date(year=2004, month=12, day=2),
                                                       datetime.time(hour=14,minute=30).strftime("%I:%M %p")))
        pass

    def submit_entry(self):
        print(self.table.item(self.table.focus()).values())
        #tab.send(s)

        pass




GUI()