import datetime

class Item:

    def __init__(self, name):
        # these are the required arguments; this will be largely mirrored in the DB
        self.name = name
        self.quantity = 0 # these are the defaults to be updated in the main.py
        self.quantity_unit = ""
        self.department = ""
        self.collected = 0
        # optional ones
        self.isle = 0
        self.store = ""

    def add_item(self):
        # returns the sqlite command as a string to populate the db w/ the item to add
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # unsure if this will just output a current datetime string or not but its worth trying
        db_query = f"INSERT INTO items (name, quantity, unit_id, department_id, isle, collected, store_id, time_created) VALUES ('{self.name}', {self.quantity}, '{self.quantity_unit}', '{self.department}', '{self.isle}', '{self.collected}', '{self.store}', '{current_time}');"
        return db_query

    def item_collected(self):
        # this is to be paired w/ a db update for the entry, update the entry's collected status to 1
        # when removing collected items in mass later, it will be a db delete where self.collected is 1
        self.collected = 1

    def __str__(self):
        print('Item: ', self.name)
        print('Quantity: ', self.quantity, " ", self.quantity_unit)
        print("Department: ", self.department)
        print("Isle: ", self.isle)
        print("Store: ", self.store)
        print("Collected? ", self.collected)