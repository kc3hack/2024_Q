import hashlib
import sqlite3
from sqlite3 import Connection, Error

from flask import flash

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
            "state":"INTEGER"
        }
        # self.user_table.table_reset(self.conn)
        self.user_table.create_table(self.conn,User.table_name,self.column_list)
    
    def create_password_hash(password):
        text = password.encode('utf-8')
        result = hashlib.sha512(text).hexdigest()
        return result
    
    def create_user(self,userName,email,password,state):
        if len(password) < 8:
            return flash('パスワードは8文字以上で設定してください')
        else:
            passwordHash = User.create_password_hash(password)
        item_list = {
        'userName':userName,
        'email':email,
        'passwordHash':passwordHash,
        'state':state
        }

        item_lists = []
        item_lists.append(item_list)
        # emailの重複チェック
        if self.get_user_info_by_email(email):
            print('そのメールアドレスは既に登録されています')
            return flash('そのメールアドレスは既に登録されています')
        self.user_table.set_table(self.conn,User.table_name)
        self.user_table.insert_table(self.conn,item_lists)

    def get_user_info(self,id):
        condition = f"id={id}"
        self.user_table.set_table(self.conn,User.table_name)
        tmp = self.user_table.select_table(self.conn,condition)
        if not tmp:
            return None
        user_info = tmp[0]
        return user_info

    def get_user_info_by_email(self,email):
        condition = f"email='{email}'"
        self.user_table.set_table(self.conn,User.table_name)
        tmp = self.user_table.select_table(self.conn,condition)
        if not tmp:
            return None
        user_info = tmp[0]
        return user_info

    def delete_user(self,id):
        self.user_table.set_table(self.conn,User.table_name)
        condition =  f'id={id}'
        self.user_table.update_table(self.conn,condition,{'state':2})
    
    def password_check(self,id,password):
        # print('test')
        # print(self.get_user_info(id))
        # print('test')
        passwordHash = self.get_user_info(id)[3]
        check = False
        if User.create_password_hash(password) == passwordHash:
            check = True
        return check

    def update_user(self,id,userName,email):
        self.user_table.set_table(self.conn,User.table_name)
        condition = f'id={id}'
        self.user_table.update_table(self.conn,condition,{'userName':userName,'email':email})
        self.user_table.set_table(self.conn,User.table_name)
        condition = f'id={id}'
        self.user_table.update_table(self.conn,condition,{'userName':userName,'email':email})
