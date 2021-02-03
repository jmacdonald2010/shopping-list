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