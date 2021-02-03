from item import Item
import sqlite3

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
conn.execute("INSERT INTO units (unit_name) VALUES ('each'), ('lbs'), ('oz'), ('mL'), ('L'), ('gallons');")
conn.execute("INSERT INTO stores (store_name) VALUES ('kroger westerville'), ('costco easton'), ('costco polaris'), ('kroger stoneridge'), ('aldi westerville');")
conn.execute("INSERT INTO departments (department_name) VALUES ('produce'), ('deli/bakery'), ('meat'), ('grocery'), ('beer/wine'), ('liquor'), ('dairy'), ('frozen'), ('pharmacy'), ('electronics'), ('other');")

print('database initialized')