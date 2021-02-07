from item import Item
import sqlite3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

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
# there may be an error w/ my sqllite commands here, but i am not sure, haven't run them yet
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
'''conn.execute("INSERT INTO units (unit_name) VALUES ('each'), ('lbs'), ('oz'), ('mL'), ('L'), ('gallons');")
conn.execute("INSERT INTO stores (store_name) VALUES ('kroger westerville'), ('costco easton'), ('costco polaris'), ('kroger stoneridge'), ('aldi westerville');")
conn.execute("INSERT INTO departments (department_name) VALUES ('produce'), ('deli/bakery'), ('meat'), ('grocery'), ('beer/wine'), ('liquor'), ('dairy'), ('frozen'), ('pharmacy'), ('electronics'), ('other');")'''

print('database initialized')
units = []
cursor = conn.execute("SELECT unit_name FROM units;")
for unit in cursor:
    units.append(unit)

# get a list of units

Builder.load_file('main.kv')

class MainScreen(Screen):
    pass

class AddItems(Screen):

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
                unit_id = units.index(text) + 1
                new_item.quantity_unit = unit_id # this will be its own unique challenge since I want to limit the options for units.
            elif field == 'Department':
                department_id = departments.index(text) + 1
                new_item.department = department_id
            elif field == 'Isle':
                new_item.isle = text
            elif field == 'Store':
                store_id = stores.index(text) + 1
                new_item.store = store_id # sim. to units, want limited options here.
        except NameError:
            print("Provide an Item name before entering other characteristics.")

    def write_to_db(self, **kwargs):
        # this may require some kind of an input to add the item to the db, but we'll get to that when we get there
        # for now, let's just try to call this function from kv
        # try:
            # print("This will eventually write to the db!")
        conn.execute(new_item.add_item())
        conn.commit()
        print('Added Item to DB')
        # except NameError:
            # print("Please ensure that all fields are completed prior to adding the item.")

    def get_units(self, **kwargs):
        global units
        units = []
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
        departments = []
        cursor = conn.execute("SELECT department_name FROM departments;")
        for department in cursor:
            departments.append(department[0])
        return departments

    def department_spinner(self, text, **kwargs):
        print(text)

    def pop_store_spinner(self, **kwargs):
        global stores
        stores = []
        cursor = conn.execute("SELECT store_name FROM stores;")
        for store in cursor:
            stores.append(store[0])
        return stores
        
    def store_spinner(self, text, **kwargs):
        print(text)

class MainApp(App):
    def build(self):
        # return main_layout
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='MainScreen'))
        sm.add_widget(AddItems(name='AddItems'))
        return sm

# code to add item should be like
# conn.execute(bananas.add_item())

if __name__ == '__main__':
    app = MainApp()
    app.run()
conn.close()