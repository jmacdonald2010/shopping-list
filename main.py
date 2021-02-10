from item import Item
import sqlite3
from kivy.app import App, runTouchApp
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
import pandas as pd
import numpy as np

# connect to db, or create if not exists
conn = sqlite3.connect('shoppingList.db')

# create tables
# start w/ creating a table for the units, then store, then departments
conn.execute('''CREATE TABLE IF NOT EXISTS units (
    unit_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    unit_name TEXT NOT NULL
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS stores(
    store_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    store_name TEXT NOT NULL
);''')

conn.execute('''CREATE TABLE IF NOT EXISTS departments(
    department_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    department_name TEXT NOT NULL
);''')

# create item table, foreign keys are quantity_unit, department, store
conn.execute('''CREATE TABLE IF NOT EXISTS items(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    quantity TEXT NOT NULL,
    unit_id INT NOT NULL,
    department_id INT NOT NULL,
    isle INT,
    collected INT NOT NULL,
    store_id TEXT,
    time_created TEXT NOT NULL,
    FOREIGN KEY (unit_id)
        REFERENCES units (unit_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (department_id)
        REFERENCES departments (department_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (store_id)
        REFERENCES stores (store_id)
        ON UPDATE CASCADE
        ON DELETE CASCADE

);

''')

# after creating the tables, populate the units, stores, and departments tables with ordinary information
# users will be given the ability to add stores and departments, but not diff. units
# starts w/ units, then stores, then departments
# NOTE!!!! this needs to be made more robust 
# this needs to be set so if those values are MISSING, it adds them, OTHERWISE, it does nothing
'''conn.execute("INSERT INTO units (unit_name) VALUES ('each'), ('lbs'), ('oz'), ('mL'), ('L'), ('gallons');")
conn.execute("INSERT INTO stores (store_name) VALUES ('kroger westerville'), ('costco easton'), ('costco polaris'), ('kroger stoneridge'), ('aldi westerville');")
conn.execute("INSERT INTO departments (department_name) VALUES ('produce'), ('deli/bakery'), ('meat'), ('grocery'), ('beer/wine'), ('liquor'), ('dairy'), ('frozen'), ('pharmacy'), ('electronics'), ('other');")'''

print('database initialized')

# Builder.load_file('main.kv') # i may not needs this line

class MainScreen(Screen, GridLayout):
    
    produce_table = ObjectProperty(None)
    deli_bakery_table = ObjectProperty(None)
    meat_table = ObjectProperty(None)
    grocery_table = ObjectProperty(None)
    beer_wine_table = ObjectProperty(None)
    liquor_table = ObjectProperty(None)
    dairy_table = ObjectProperty(None)
    frozen_table = ObjectProperty(None)
    pharmacy_table = ObjectProperty(None)
    electronics_table = ObjectProperty(None)
    other_table = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # load the data into the accordionItem tables
        # first, load all of the data
        # first, create a produce df
        # NOTE something I worry about here is if these dataframes will get actively updated when I add items from the other screen.
        self.produce_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id FROM items WHERE department_id = 1;', conn, index_col='name')
        print(self.produce_df)
        self.deli_bakery_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id FROM items WHERE department_id = 2;', conn, index_col='name')
        print(self.deli_bakery_df)



class AddItems(Screen):
    # object properties not yet tested
    unit = ObjectProperty(None)
    store: ObjectProperty(None)
    department: ObjectProperty(None)
    item = ObjectProperty(None)
    quantity = ObjectProperty(None)
    isle = ObjectProperty(None)

    def add_new_item(self, value):
        # creating a new object
        global new_item
        new_item = Item(value)
        return new_item

    def update_item_value(self, field, text):
        try:
            if field == 'Quantity':
                new_item.quantity = text
                print(new_item.quantity)
            elif field == 'Unit':
                unit_id = units.index(text)
                new_item.quantity_unit = unit_id 
            elif field == 'Department':
                department_id = departments.index(text)
                new_item.department = department_id
            elif field == 'Isle':
                new_item.isle = text
            elif field == 'Store':
                store_id = stores.index(text)
                new_item.store = store_id 
        except NameError:
            print("Provide an Item name before entering other characteristics.")

    def write_to_db(self, **kwargs):
        try:
            if (self.department.text == 'Departments') | (self.unit.text == 'Units') | (self.store.text == 'Stores') | (self.item.text == '') | (self.quantity.text == ''):
                print('Please ensure that all fields are completed prior to adding the item.')
            else:
                conn.execute(new_item.add_item())
                conn.commit()
                print('Added Item to DB')
                self.clear_inputs()
        except (NameError, sqlite3.OperationalError) as e:
            print("Please ensure that all fields are completed prior to adding the item.")

    def get_units(self, **kwargs):
        global units
        units = ["Units"]
        cursor = conn.execute("SELECT unit_name FROM units;")
        for unit in cursor:
            units.append(unit[0])
        return units

    def unit_spinner(self, text, **kwargs):
        try:
            new_item.quantity_unit = text
        except NameError:
            print("Need to provide an item name first!")

    def pop_department_spinner(self, **kwargs):
        global departments
        departments = ["Departments"]
        cursor = conn.execute("SELECT department_name FROM departments;")
        for department in cursor:
            departments.append(department[0])
        return departments

    def department_spinner(self, text, **kwargs):
        print(text)

    def pop_store_spinner(self, **kwargs):
        global stores
        stores = ["Stores"]
        cursor = conn.execute("SELECT store_name FROM stores;")
        for store in cursor:
            stores.append(store[0])
        return stores
        
    def store_spinner(self, text, **kwargs):
        print(text)

    def clear_inputs(self):
        self.item.text = ''
        self.quantity.text = ''
        self.isle.text = ''
        self.unit.text = "Units"
        self.department.text = "Departments"
        self.store.text = "Stores"
            

class MainApp(App):
    def build(self):
        # return main_layout
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='MainScreen'))
        sm.add_widget(AddItems(name='AddItems'))
        return sm

# code to add item should be like
# conn.execute(bananas.add_item())

# runTouchApp(MainApp)

if __name__ == '__main__':
    app = MainApp()
    app.run()
    #runTouchApp()
conn.close()