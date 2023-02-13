import sqlite3

from constants import APP, BLUEPRINT, API, DATABASE
from user import user_namespace
from device import device_namespace#, id_namespace
from access import access_namespace

# Database setup
connection = sqlite3.connect(DATABASE)
cursor = connection.cursor()

# Define tables
def create_users_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS
        users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            password TEXT NOT NULL)""")

def create_devices_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS
        devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial TEXT NOT NULL,
            name TEXT NOT NULL)""")

def create_accesses_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS
        accesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            device_id INTEGER NOT NULL,
            FOREIGN KEY (device_id) REFERENCES devices(id),
            FOREIGN KEY (user_id) REFERENCES users(id))""")

# create tables
create_users_table()
create_devices_table()
create_accesses_table()
connection.commit()

# add namespaces
# API.add_namespace(id_namespace)
API.add_namespace(user_namespace)
API.add_namespace(device_namespace)
API.add_namespace(access_namespace)

# register blueprint
APP.register_blueprint(BLUEPRINT)

# run the app
if __name__ == '__main__':
    APP.run(debug=True)