import sqlite3
from sqlite3 import Connection, Error
from db.database import Table

class user():
    def __init__(self):
        user_table = Table()
        con = user_table.create_connection('sns_data.db')
        if user_table.check_table():

        