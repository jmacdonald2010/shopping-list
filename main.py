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
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.properties import ObjectProperty
import pandas as pd
import numpy as np
# from collections import Counter

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
    # allows us to add accordion items to the Accordion in the main.kv file.
    shopping_list = ObjectProperty(None)
    # accordion_size = ObjectProperty(None)


    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        # build the main screen; is its own function since we call on it while the app is still running.
        # stores_dict_init = 0
        accordion_size = 1000
        MainScreen.build_accordions(self)

    @classmethod
    def calc_accordion_size(cls, **kwargs):
        # might just be able to start here
        dbq = pd.read_sql('SELECT id, department_id FROM items;', conn)
        dept_counts = dbq['department_id'].value_counts()
        biggest_val = dept_counts.idxmax(axis=1)
        # biggest_val = 0
        # for key, val in item_no_dict.items():
        #     if biggest_val == 0:
        #         biggest_val = val
        #     elif val > biggest_val:
        #         biggest_val = val
        calcd_size = dept_counts[biggest_val] * 100
        return int(calcd_size)

    @classmethod
    def build_accordions(cls, self, **kwargs):
        # create lists of the departments
        departments = []
        department_ids =[]
        departments_q = conn.execute('SELECT * FROM departments;')
        departments_q = departments_q.fetchall()
        for department in departments_q:
            department_id = department[0]
            department_name = department[1]
            department_ids.append(department_id)
            departments.append(department_name)
        
        # create dict of stores and their ids
        global current_store
        global stores_dict_init
        global stores_dict
        try:
            if stores_dict_init == 1:
                pass
        except NameError:
            stores_dict = dict()
            stores_dict_q = conn.execute('SELECT store_name, store_id FROM stores;')
            stores_dict_q = stores_dict_q.fetchall()
            for store in stores_dict_q:
                stores_dict[store[0]] = store[1]
                if store[1] == 1:
                    current_store = store[0]
            stores_dict_init = 1

        # current_store = 

        # declare for later
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
            department_dfs[id] = pd.read_sql(f'SELECT name, quantity, unit_id, isle, collected, store_id, id, time_created FROM items WHERE department_id = {id} AND store_id = {stores_dict[current_store]};', conn, index_col='name')

            department_dfs[id] = department_dfs[id].sort_values('isle')

            # iterate thru the DF and create labels for them; not adding button binding functionality yet
            for row in department_dfs[id].itertuples():
                toggles[row[6]] = ToggleButton(state=MainScreen.check_toggle_state(row[4], row[6]))
                department_grid.add_widget(toggles[row[6]])
                department_grid.add_widget(Label(text=str(row[0]), text_size= (self.width, None)))
                department_grid.add_widget(Label(text=str(row[1])))
                department_grid.add_widget(Label(text=unit_dict[row[2]]))
                department_grid.add_widget(Label(text=str(row[3])))
                department_grid.add_widget(Label(text=str(row[7]), text_size= (self.width, None)))
            
            # get the keys and vals in ordered lists
            global toggles_key_list
            toggles_key_list = []
            global toggles_val_list
            toggles_val_list = []
            for key, val in toggles.items():
                toggles_key_list.append(key)
                toggles_val_list.append(val)

            # add functionality to the toggle buttons
            toggles_lambdas = dict()
            for button in department_grid.children[1:]:
                if isinstance(button, ToggleButton):
                    for key, value in toggles.items():
                        if button == value:
                            # self.toggle_id = self.produce_toggles_key_list.index(key)
                            toggles_lambdas[key] = lambda key: MainScreen.change_toggle_state(key)
                            button.bind(on_press= toggles_lambdas[key])
        #  <<<<<<<<<<<<<<<< Settings Menu >>>>>>>>>>>>>>>>>>

        # add a settings accordion item
        settings_accordion = AccordionItem(orientation='vertical', title='Settings')
        # create the grid for the accordion item
        settings_grid = GridLayout(cols=1, padding = [1, 1, 1, 1])
        # add the accordion item to the accordion, then add the grid to that accordion item
        self.shopping_list.add_widget(settings_accordion)
        settings_accordion.add_widget(settings_grid)
        
        #  <<<<<<<<<<<<<<<< Delete Button >>>>>>>>>>>>>>>>>>
        # add buttons to the settings menu
        # first, the delete all items button
        delete_all_items = Button(text='Delete All Items')

        # create a popup item for the above button
        global delete_popup
        delete_popup = Popup(title='Delete All Items',size_hint=(None,None), size=(400,400))

        # create a grid layout for the delete popup, add the grid to the popup
        delete_grid = GridLayout(cols=1, padding=[.2, .2, .2, .2])
        delete_popup.add_widget(delete_grid)

        # add 'are you sure?' delete all items button to the popup grid
        you_sure_delete = Button(text="Are you Sure? This is irreversable! This will delete items from ALL stores!")
        you_sure_delete.bind(on_press= lambda x2: MainScreen.delete_all_items_func(self))
        delete_grid.add_widget(you_sure_delete)

        # add a cancel button as well
        cancel_delete = Button(text="Cancel")
        cancel_delete.bind(on_press= lambda xx: delete_popup.dismiss())
        delete_grid.add_widget(cancel_delete)

        # bind the opening of the popup to the button
        delete_all_items.bind(on_press= lambda x: delete_popup.open())
        # add the delete button to the settings grid
        settings_grid.add_widget(delete_all_items)

        #  <<<<<<<<<<<<<<<< Add Store Button >>>>>>>>>>>>>>>>>>

        # add an add store button
        add_store = Button(text='Add Store') # launches the popup
        global add_store_popup
        add_store_popup = Popup(title='Add Store (REQUIRES RELAUNCH TO REFLECT CHANGES)', size_hint=(None, None), size=(400, 400)) # is the popup
        add_store_grid = GridLayout(cols=1, padding=[.2, .2, .2, .2]) # grid layout for popup
        add_store_popup.add_widget(add_store_grid)
        add_store_text = TextInput(hint_text='Type Store Name Here', multiline=False) # text input for stores
        add_store_text.bind(on_text= lambda asct: MainScreen.add_store_func(self, 0))
        add_store_grid.add_widget(add_store_text)
        add_store_button = Button(text='Add Store')
        add_store_button.bind(on_press= lambda ast: MainScreen.add_store_func(self, add_store_text.text, 1))
        add_store_grid.add_widget(add_store_button)
        add_store_cancel = Button(text="Cancel") # cancel button for popup
        add_store_cancel.bind(on_press= lambda asc: add_store_popup.dismiss())
        add_store_grid.add_widget(add_store_cancel)
        # add_store_grid.add_widget(add_store_cancel)
        add_store.bind(on_press= lambda asb: add_store_popup.open())
        settings_grid.add_widget(add_store)

        #  <<<<<<<<<<<<<<<< Add Departments >>>>>>>>>>>>>>>>>>
        add_department = Button(text='Add Department') # define button in settings grid
        global add_department_popup
        add_department_popup = Popup(title='Add Department (REQUIRES RELAUNCH TO REFLECT CHANGES)', size_hint=(None, None), size=(400, 400)) # define popup from add_department
        add_department_grid = GridLayout(cols=1, padding=[.2, .2, .2, .2]) # define grid to add to the popup
        add_department_popup.add_widget(add_department_grid) # add grid to popup
        add_department_text = TextInput(hint_text='Type Department Name Here', multiline=False) # text entry box for the grid
        add_department_text.bind(on_text= lambda adt: MainScreen.add_department_func(self, 0)) # bind the function to the text entry
        add_department_grid.add_widget(add_department_text) # add text entry to the grid
        add_department_button = Button(text='Add Department') # button to add text to db, will be added to grid
        add_department_button.bind(on_press= lambda adb: MainScreen.add_department_func(self, add_department_text.text, 1)) # binds function to button
        add_department_grid.add_widget(add_department_button)
        add_department_cancel = Button(text='Cancel')
        add_department_cancel.bind(on_press= lambda adc: add_department_popup.dismiss())
        add_department_grid.add_widget(add_department_cancel)
        add_department.bind(on_press= lambda add: add_department_popup.open())
        settings_grid.add_widget(add_department)
        
        # <<<<<<<<<< Change Store Spinner >>>>>>>>>>>>>>
        change_store = Button(text='Select Store')
        global change_store_popup
        change_store_popup = Popup(title='Select Store', size_hint=(None, None), size=(400,200))
        change_store_spinner = Spinner(text='Store',size=(100, 50), values=MainScreen.pop_current_store_spinner(self)) 
        change_store_spinner.bind(text=lambda change_store_spinner, css: MainScreen.change_store_spinner_func(self,change_store_spinner.text))
        change_store_popup.add_widget(change_store_spinner)
        change_store.bind(on_press= lambda csb: change_store_popup.open())
        settings_grid.add_widget(change_store)

        # populate recently added items on second screen
        # AddItems.recent_added_list(add_items)

    @classmethod
    def pop_current_store_spinner(cls, self, **kwargs):
        stores_list_q = conn.execute('SELECT store_name FROM stores;')
        stores_list_q = stores_list_q.fetchall()
        global stores_list
        stores_list = []
        for store in stores_list_q:
            stores_list.append(store[0])
        return stores_list
    
    @classmethod
    def change_store_spinner_func(cls, self, store, **kwargs):
        global current_store
        current_store = store
        print(current_store)
        change_store_popup.dismiss()
        MainScreen.refresh_main_screen(self)
        # return self

    @classmethod
    def delete_all_items_func(cls, self, **kwargs):
        conn.execute('DELETE FROM items;')
        conn.commit()
        print('Items table content deleted')
        delete_popup.dismiss()
        MainScreen.refresh_main_screen(self)
        # return True

    @classmethod
    def add_store_func(cls, self, text, execute, **kwargs):
        global new_store_name
        new_store_name = text
        if execute == 1:
            conn.execute(f'INSERT INTO stores (store_name) VALUES ("{new_store_name}"); ')
            conn.commit()
            print("Added store to database")
            add_store_popup.dismiss()
            execute = 0
            MainScreen.refresh_main_screen(self)

    @classmethod
    def add_department_func(cls, self, text, execute, **kwargs):
        global new_department_name
        new_department_name = text
        if execute == 1:
            conn.execute(f'INSERT INTO departments (department_name) VALUES ("{new_department_name}"); ')
            conn.commit()
            print("Added department to database")
            add_store_popup.dismiss()
            execute = 0
            MainScreen.refresh_main_screen(self)

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
    recently_added = ObjectProperty(None)
    # main_screen = MainScreen()

    def __init__(self, **kwargs):
        super(AddItems, self).__init__(**kwargs)
        AddItems.recent_added_list(self)

    #    pass

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
        AddItems.destroy_recent_added_list(self)
        AddItems.recent_added_list(self)


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

    @classmethod
    def recent_added_list(cls, self):
        # first, add the necessary labels
        self.recently_added.add_widget(Label(text='Item'))
        self.recently_added.add_widget(Label(text='Amount'))
        self.recently_added.add_widget(Label(text='Unit'))
        self.recently_added.add_widget(Label(text='Department'))
        self.recently_added.add_widget(Label(text='Isle'))
        self.recently_added.add_widget(Label(text='Store'))
        self.recently_added.add_widget(Label(text='DateTime Added'))

        # then, assemble dicts for the foreign keys in the db
        # assemble a dict of unit_id, department_id, and store_id

        # unit_id dict; hopefully this won't be an issue w/ the MainScreen class
        unit_dict_df = pd.read_sql('SELECT unit_id, unit_name FROM units;', conn)
        unit_dict = dict()
        for unit in unit_dict_df.itertuples():
            unit_dict[unit[1]] = unit[2]

        # department_id dict
        department_dict_df = pd.read_sql('SELECT department_id, department_name FROM departments;', conn)
        department_dict = dict()
        for department in department_dict_df.itertuples():
            department_dict[department[1]] = department[2]

        # store_id dict
        store_dict_df = pd.read_sql('SELECT store_id, store_name FROM stores;', conn)
        store_dict = dict()
        for store in store_dict_df.itertuples():
            store_dict[store[1]] = store[2]

        # assemble the items table as a pd df
        recent_added_df = pd.read_sql('SELECT name, quantity, unit_id, department_id, isle, store_id, time_created FROM items;', conn)
        recent_added_df = recent_added_df.sort_values('time_created', ascending=False)
        # go thru the first five items, put them in the grid layout of the add item screen
        count = 0
        for item in recent_added_df.itertuples():
            self.recently_added.add_widget(Label(text=str(item[1]), text_size=(self.width, None))) # name
            self.recently_added.add_widget(Label(text=str(item[2]))) # amt
            self.recently_added.add_widget(Label(text=str(unit_dict[int(item[3])]))) # unit
            self.recently_added.add_widget(Label(text=str(department_dict[item[4]]))) # department
            self.recently_added.add_widget(Label(text=str(item[5]))) # isle
            self.recently_added.add_widget(Label(text=str(store_dict[int(item[6])]))) # store
            self.recently_added.add_widget(Label(text=str(item[7]), text_size=(self.width, None)))
            count += 1
            if count > 5:
                break

    @classmethod
    def destroy_recent_added_list(cls, self):
        for label in self.recently_added.children[0:]:
            self.recently_added.remove_widget(label)
            

class MainApp(App):
    def build(self):
        # return main_layout
        global main_screen
        global add_items
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