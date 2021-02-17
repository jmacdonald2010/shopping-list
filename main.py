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
    shopping_list = ObjectProperty(None)
    #add_items = AddItems()


    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        MainScreen.build_accordions(self)
        # self.app = App.get_running_app()
        # self.main_screen = self.app.main_screen
        
    @classmethod
    def build_accordions(cls, self, **kwargs):
        # shopping_list = ObjectProperty(MainScreen)

        departments = []
        department_ids =[]
        departments_q = conn.execute('SELECT * FROM departments;')
        departments_q = departments_q.fetchall()
        for department in departments_q:
            department_id = department[0]
            department_name = department[1]
            department_ids.append(department_id)
            departments.append(department_name)
        
        toggles = dict()

        # dict for unit labels
        unit_dict = dict()
        units = conn.execute('SELECT * FROM units;')
        units = units.fetchall()
        for unit in units:
            unit_id = unit[0]
            unit_name = unit[1]
            unit_dict[unit_id] = unit_name


        # build the accordion items to the main screen
        department_dfs = dict()
        for department, id in zip(departments, department_ids):
            # create the accordion item
            department_accordion = AccordionItem(orientation='vertical', title=department)
            department_grid = GridLayout(cols=6)
            self.shopping_list.add_widget(department_accordion)
            department_accordion.add_widget(department_grid)

            # now populate the accordion, first the column names
            department_grid.add_widget(Label(text="Collected?"))
            department_grid.add_widget(Label(text="Item"))
            department_grid.add_widget(Label(text="Amt"))
            department_grid.add_widget(Label(text="Unit"))
            department_grid.add_widget(Label(text="Isle"))
            department_grid.add_widget(Label(text="DateTime Added"))

            # now get the data from the db
            department_dfs[id] = pd.read_sql(f'SELECT name, quantity, unit_id, isle, collected, store_id, id, time_created FROM items WHERE department_id = {id};', conn, index_col='name')

            # iterate thru the DF and create labels for them; not adding button binding functionality yet
            for row in department_dfs[id].itertuples():
                toggles[row[6]] = ToggleButton(state=MainScreen.check_toggle_state(row[4], row[6]))
                department_grid.add_widget(toggles[row[6]])
                department_grid.add_widget(Label(text=str(row[0])))
                department_grid.add_widget(Label(text=str(row[1])))
                department_grid.add_widget(Label(text=unit_dict[row[2]]))
                department_grid.add_widget(Label(text=str(row[3])))
                department_grid.add_widget(Label(text=str(row[7])))
            
            # get the keys and vals in ordered lists
            global toggles_key_list
            toggles_key_list = []
            global toggles_val_list
            toggles_val_list = []
            for key, val in toggles.items():
                toggles_key_list.append(key)
                toggles_val_list.append(val)
        
            toggles_lambdas = dict()
            # if self.produce_accordion_toggles_bound == False:
            for button in department_grid.children[1:]:
                if isinstance(button, ToggleButton):
                    for key, value in toggles.items():
                        if button == value:
                            # self.toggle_id = self.produce_toggles_key_list.index(key)
                            toggles_lambdas[key] = lambda key: MainScreen.change_toggle_state(key)
                            button.bind(on_press= toggles_lambdas[key])

    @classmethod
    def check_toggle_state(cls, state, id, **kwargs):
        # print('toggle value changes')
        if state == True:
            # conn.execute(f'UPDATE items SET collected = True WHERE id = {id}')
            # conn.commit()
            # print(conn.total_changes)
            state = 'down'
        else:
            state = 'normal'
        return state

    @classmethod
    def change_toggle_state(cls, id, **kwargs):
        id = toggles_val_list.index(id)
        id = toggles_key_list[id]
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

    @classmethod
    def remove_collected_items(cls):
        query = conn.execute('DELETE FROM items WHERE collected = 1;')
        conn.commit()
        print('deleted collected entries')
        # now delete the accordion items that are currently present so we can rebild them
        MainScreen.refresh_main_screen(main_screen)

    @classmethod
    def refresh_main_screen(cls, self):
        for accordion in self.shopping_list.children[0:]:
            self.shopping_list.remove_widget(accordion)
        MainScreen.build_accordions(self)

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
    # main_screen = MainScreen()

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
        MainScreen.refresh_main_screen(main_screen)


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
        global main_screen
        main_screen = MainScreen(name='MainScreen')
        add_items = AddItems(name='AddItems')
        sm = ScreenManager()
        sm.add_widget(main_screen)
        sm.add_widget(add_items)
        return sm

# code to add item should be like
# conn.execute(bananas.add_item())

# runTouchApp(MainApp)

if __name__ == '__main__':
    app = MainApp()
    app.run()
    #runTouchApp()
conn.close()