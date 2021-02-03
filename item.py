import datetime

class Item:

    def __init__(self, name, quantity, quantity_unit, department, collected):
        # these are the required arguments; this will be largely mirrored in the DB
        self.name = name
        self.quantity = quantity
        self.quantity_unit = quantity_unit
        self.department = department
        self.collected = collected
        # optional ones
        self.isle = 0
        self.store = ""

    def add_item(self):
        # returns the sqlite command as a string to populate the db w/ the item to add
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # unsure if this will just output a current datetime string or not but its worth trying
        db_query = f"INSERT INTO items (name, quantity, unit_id, department_id, isle, collected, store_id, time_created) VALUES ('{self.name}', {self.quantity}, '{self.quantity_unit}', {self.department}, {self.isle}, {self.collected}, {self.store_id}, '{current_time}');"
        return db_query

    def item_collected(self):
        # this is to be paired w/ a db update for the entry, update the entry's collected status to 1
        # when removing collected items in mass later, it will be a db delete where self.collected is 1
        self.collected = 1