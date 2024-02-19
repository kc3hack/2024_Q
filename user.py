import sqlite3,hashlib
from sqlite3 import Connection, Error
from db.database import Table

class User():
    table_name = 'user'
    def __init__(self):
        self.user_table = Table()
        self.conn = self.user_table.create_connection('sns_data.db')
        self.column_list = {
            "userName":"TEXT",
            "email":"TEXT",
            "passwordHash":"TEXT",
            "createdAt":"INTEGER",
            "state":"INTEGER"
        }
        self.user_table.create_table(self.conn,User.table_name,self.column_list)
    
    def create_password_hash(password):
        text = password.encode('utf-8')
        result = hashlib.sha512(text).hexdigest
        return result
    
    def create_user(self,userName,email,password,createdAt,state):
        if passwordHash < 8:
            return"パスワードが小さすぎます"
        else:
            passwordHash = User.create_password_hash(password)
        item_list = {
        'userName':userName,
        'email':email,
        'passwordHash':passwordHash,
        'createdAt':createdAt,
        'state':state
        }
        item_lists = []
        item_lists.append(item_list)

    def get_user_info(self,id):
        condition = f"id={id}"
        columns = ['userName','email','passwordHash','createdAt','state']
        user_info = self.user_table.select_table(self.conn,condition)
       
        user_info_dict = dict(zip(columns,user_info))

        return user_info_dict





        