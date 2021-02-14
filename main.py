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
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
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
    produce_grid = ObjectProperty(None)
    deli_bakery_table = ObjectProperty(None)
    deli_bakery_grid = ObjectProperty(None)
    meat_table = ObjectProperty(None)
    meat_grid = ObjectProperty(None)
    grocery_table = ObjectProperty(None)
    grocery_grid = ObjectProperty(None)
    beer_wine_table = ObjectProperty(None)
    beer_wine_grid = ObjectProperty(None)
    liquor_table = ObjectProperty(None)
    liquor_grid = ObjectProperty(None)
    dairy_table = ObjectProperty(None)
    dairy_grid = ObjectProperty(None)
    frozen_table = ObjectProperty(None)
    frozen_grid = ObjectProperty(None)
    pharmacy_table = ObjectProperty(None)
    pharmacy_grid = ObjectProperty(None)
    electronics_table = ObjectProperty(None)
    electronics_grid = ObjectProperty(None)
    other_table = ObjectProperty(None)
    other_grid = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # load the data into the accordionItem tables
        # first, load all of the data
        # first, create a produce df
        # NOTE something I worry about here is if these dataframes will get actively updated when I add items from the other screen.
        # I think it may also be easier to do join statements to populate the actual department names, unit names, store names, etc.
        self.produce_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id, id, time_created FROM items WHERE department_id = 1;', conn, index_col='name')
        # print(self.produce_df)
        self.deli_bakery_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id, id FROM items WHERE department_id = 2;', conn, index_col='name')
        # print(self.deli_bakery_df)
        self.meat_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id, id FROM items WHERE department_id = 3;', conn, index_col='name')
        self.grocery_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id, id FROM items WHERE department_id = 4;', conn, index_col='name')
        self.beer_wine_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id, id FROM items WHERE department_id = 5;', conn, index_col='name')
        self.liquor_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id, id FROM items WHERE department_id = 6;', conn, index_col='name')
        self.dairy_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id, id FROM items WHERE department_id = 7;', conn, index_col='name')
        self.frozen_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id, id FROM items WHERE department_id = 8;', conn, index_col='name')
        self.pharmacy_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id, id FROM items WHERE department_id = 9;', conn, index_col='name')
        self.electronics_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id, id FROM items WHERE department_id = 10;', conn, index_col='name')
        self.other_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id, id FROM items WHERE department_id = 11;', conn, index_col='name')

        # first, I think I need to set the grid layout from within here
        # self.produce_table = GridLayout(cols=5)

        # attempt to create the contents of the accordion item here and not in kv b/c it's dynamic
        # build produce accordion contents
        '''self.produce_grid.add_widget(Label(text='Collected?')) # blank b/c checkbox
        self.produce_grid.add_widget(Label(text='Item'))
        self.produce_grid.add_widget(Label(text='Amt'))
        self.produce_grid.add_widget(Label(text='Unit'))
        self.produce_grid.add_widget(Label(text='Isle'))
        self.produce_grid.add_widget(Label(text='DateTime Added'))

        self.toggles = dict()
        for row in self.produce_df.itertuples():
            self.toggles[row[6]] = ToggleButton(state=self.check_toggle_state(row[4], row[6]))
            self.toggles[row[6]].bind(on_press=lambda x:self.change_toggle_state(row[4], row[6]))
            # self.toggle = ToggleButton(state=self.check_toggle_state(row[4], row[6]))
            # self.toggle.bind(on_press=lambda x:self.change_toggle_state(row[4], row[6]))
            #self.produce_grid.add_widget(ToggleButton(state=self.check_toggle_state(row[4], row[6])).bind(on_press=lambda x:self.change_toggle_state(row[4], row[6])))
            self.produce_grid.add_widget(self.toggles[row[6]])
            self.produce_grid.add_widget(Label(text=str(row[0])))
            self.produce_grid.add_widget(Label(text=str(row[1])))
            self.produce_grid.add_widget(Label(text=str(row[2])))
            self.produce_grid.add_widget(Label(text=str(row[3])))
            self.produce_grid.add_widget(Label(text=str(row[7])))'''
            
            # pass

        self.deli_bakery_table.add_widget(Label(text='')) # blank b/c checkbox
        self.deli_bakery_table.add_widget(Label(text='Item'))
        self.deli_bakery_table.add_widget(Label(text='Amt'))
        self.deli_bakery_table.add_widget(Label(text='Unit'))
        self.deli_bakery_table.add_widget(Label(text='Isle'))        
        
        self.meat_table.add_widget(Label(text='')) # blank b/c checkbox
        self.meat_table.add_widget(Label(text='Item'))
        self.meat_table.add_widget(Label(text='Amt'))
        self.meat_table.add_widget(Label(text='Unit'))
        self.meat_table.add_widget(Label(text='Isle'))

        self.grocery_table.add_widget(Label(text='')) # blank b/c checkbox
        self.grocery_table.add_widget(Label(text='Item'))
        self.grocery_table.add_widget(Label(text='Amt'))
        self.grocery_table.add_widget(Label(text='Unit'))
        self.grocery_table.add_widget(Label(text='Isle'))

        self.beer_wine_table.add_widget(Label(text='')) # blank b/c checkbox
        self.beer_wine_table.add_widget(Label(text='Item'))
        self.beer_wine_table.add_widget(Label(text='Amt'))
        self.beer_wine_table.add_widget(Label(text='Unit'))
        self.beer_wine_table.add_widget(Label(text='Isle'))

        self.liquor_table.add_widget(Label(text='')) # blank b/c checkbox
        self.liquor_table.add_widget(Label(text='Item'))
        self.liquor_table.add_widget(Label(text='Amt'))
        self.liquor_table.add_widget(Label(text='Unit'))
        self.liquor_table.add_widget(Label(text='Isle'))

        self.dairy_table.add_widget(Label(text='')) # blank b/c checkbox
        self.dairy_table.add_widget(Label(text='Item'))
        self.dairy_table.add_widget(Label(text='Amt'))
        self.dairy_table.add_widget(Label(text='Unit'))
        self.dairy_table.add_widget(Label(text='Isle'))

        self.frozen_table.add_widget(Label(text='')) # blank b/c checkbox
        self.frozen_table.add_widget(Label(text='Item'))
        self.frozen_table.add_widget(Label(text='Amt'))
        self.frozen_table.add_widget(Label(text='Unit'))
        self.frozen_table.add_widget(Label(text='Isle'))

        self.pharmacy_table.add_widget(Label(text='')) # blank b/c checkbox
        self.pharmacy_table.add_widget(Label(text='Item'))
        self.pharmacy_table.add_widget(Label(text='Amt'))
        self.pharmacy_table.add_widget(Label(text='Unit'))
        self.pharmacy_table.add_widget(Label(text='Isle'))

        self.electronics_table.add_widget(Label(text='')) # blank b/c checkbox
        self.electronics_table.add_widget(Label(text='Item'))
        self.electronics_table.add_widget(Label(text='Amt'))
        self.electronics_table.add_widget(Label(text='Unit'))
        self.electronics_table.add_widget(Label(text='Isle'))

        self.other_table.add_widget(Label(text='')) # blank b/c checkbox
        self.other_table.add_widget(Label(text='Item'))
        self.other_table.add_widget(Label(text='Amt'))
        self.other_table.add_widget(Label(text='Unit'))
        self.other_table.add_widget(Label(text='Isle'))

        # this is to help out the build_department_accordion funcs
        self.produce_accordion_labels_added = False
        self.produce_accordion_items_added = []
        self.toggles = dict()
        self.produce_accordion_toggles_bound = False


    def build_produce_accordion(self, **kwargs):
        # reread the db every time the menu is opened
        self.produce_df = pd.read_sql('SELECT name, quantity, unit_id, isle, collected, store_id, id, time_created FROM items WHERE department_id = 1;', conn, index_col='name')
        # add the top labels
        if self.produce_accordion_labels_added == False:
            self.produce_grid.add_widget(Label(text='Collected?'))
            self.produce_grid.add_widget(Label(text='Item'))
            self.produce_grid.add_widget(Label(text='Amt'))
            self.produce_grid.add_widget(Label(text='Unit'))
            self.produce_grid.add_widget(Label(text='Isle'))
            self.produce_grid.add_widget(Label(text='DateTime Added'))

        self.produce_accordion_labels_added = True

        # fill the accordion
        for row in self.produce_df.itertuples():
            if row[6] in self.produce_accordion_items_added:
                continue
            else:
                self.toggles[row[6]] = ToggleButton(state=self.check_toggle_state(row[4], row[6]))
                # self.toggles[row[6]].bind(on_press= lambda x:self.toggle_test_func(row[6]))
                #self.toggles[row[6]].bind(on_press=lambda x:self.change_toggle_state(row[4], row[6]))
                # self.toggle = ToggleButton(state=self.check_toggle_state(row[4], row[6]))
                # self.toggle.bind(on_press=lambda x:self.change_toggle_state(row[4], row[6]))
                #self.produce_grid.add_widget(ToggleButton(state=self.check_toggle_state(row[4], row[6])).bind(on_press=lambda x:self.change_toggle_state(row[4], row[6])))
                self.produce_grid.add_widget(self.toggles[row[6]])
                self.produce_grid.add_widget(Label(text=str(row[0])))
                self.produce_grid.add_widget(Label(text=str(row[1])))
                self.produce_grid.add_widget(Label(text=str(row[2])))
                self.produce_grid.add_widget(Label(text=str(row[3])))
                self.produce_grid.add_widget(Label(text=str(row[7])))
                self.produce_accordion_items_added.append(row[6])
        
        '''i = 0
        for button in self.produce_grid.children[1:]:
            button.bind(on_press= lambda x: self.toggle_test_func('test'))'''

        # this is so I can actually get the item ID # assoc. w/ the button to bind to the function properly
        self.produce_toggles_key_list = []
        self.produce_toggles_val_list = []
        for key, val in self.toggles.items():
            self.produce_toggles_key_list.append(key)
            self.produce_toggles_val_list.append(val)

        self.produce_lambdas = dict()
        # if self.produce_accordion_toggles_bound == False:
        for button in self.produce_grid.children[1:]:
            if isinstance(button, ToggleButton):
                for key, value in self.toggles.items():
                    if button == value:
                        # self.toggle_id = self.produce_toggles_key_list.index(key)
                        self.produce_lambdas[key] = lambda key: self.change_toggle_state(key)
                        button.bind(on_press= self.produce_lambdas[key])
            # self.produce_accordion_toggles_bound = True



    def check_toggle_state(self, state, id, **kwargs):
        # print('toggle value changes')
        if state == True:
            # conn.execute(f'UPDATE items SET collected = True WHERE id = {id}')
            # conn.commit()
            # print(conn.total_changes)
            state = 'down'
        else:
            state = 'normal'
        return state

    def change_toggle_state(self, id, **kwargs):
        id = self.produce_toggles_val_list.index(id)
        id = self.produce_toggles_key_list[id]
        state = conn.execute(f'SELECT collected FROM items WHERE id = {id}')
        state = state.fetchall()
        state = state[0]
        if state[0] == 0:
            conn.execute(f'UPDATE items SET collected = 1 WHERE id = {id}')
            conn.commit()
            print(conn.total_changes)
            state = 'normal'
        elif state[0] == 1:
            conn.execute(f'UPDATE items SET collected = 0 WHERE id = {id}')
            conn.commit()
            print(conn.total_changes)
            state = 'down'
        return state[0]

    def toggle_test_func(self, id):
        print(id)
        
    '''def test_func(self):
        print('test func ran')'''

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