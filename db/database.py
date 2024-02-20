import sqlite3
from sqlite3 import Connection, Error

# TODO コードをきれいに、あとコメントも
# TODO 例外処理を入れる
# TODO 動作確認
# TODO sqlインジェクション対策

class Table():
    def __init__(self):
        self.colum_detail = None
        self.table_name = ""

    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)
        return conn
    
    def set_table(self,conn,table_name):
        info = None
        cor = conn.cursor()
        try:
            info_sql = cor.execute('PRAGMA table_info({})'.format(table_name))
        except Error as e:
            print(e)
        else:
            self.table_name = table_name
            info = info_sql.fetchall()
            for i in range(info[1]):
                self.colum_detail.append([info[1][i],info[2][i]])


    def close_connection(conn):
        conn.close()
        

    def check_table(self,conn,table_name):
        cor = conn.cursor()
        cor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        info = cor.fetchall()
        for table in info:
            if table[0] == table_name:
                return True
        return False

        

    def create_table(self,conn,table_name:str, column_list:dict):
        if not self.check_table(conn,table_name):
            cor = conn.cursor()
            # CREATE TABLE文の基本形を作成
            create_table_sql = "CREATE TABLE " + table_name + " (id INTEGER PRIMARY KEY AUTOINCREMENT"
            
            # 辞書からカラム名とデータ型を取得してSQL文に追加
            # columns_sql = ', '.join([f"{column_name} {data_type}" for column_name, data_type in column_list.items()])
            # SQLite の 柔軟な型付け(flexible typing)機能のおかげで、データ型の指定はオプションになっています。(公式ドキュメント曰く)
            # なのでdatatypeをカット
            columns_sql = ""
            for colum_name,data_type in column_list.items():
                colums_sql += "," + colum_name
                self.colum_detail.append([colum_name,data_type])
            # カラム定義をSQL文に追加し、最終的なSQL文を完成させる
            create_table_sql += columns_sql + "created_at DEFAULT (DATETIME('now','localtime')) )"
            try:
                # SQL文を実行
                cor.execute(create_table_sql)
                print("Table created successfully")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        else:
            print("Table already exists")

    # TODO colum_detailに型があるので型のチェックを入れる
    def insert_table(self,conn :Connection, item_lists :list):
        cor = conn.cursor()

        datas = []
        # item_listの中身を取り出して、SQL文に埋め込める形にする
        for item_list in item_lists:
            data=[]
            # item_listの中身を取り出して、SQL文に埋め込める形にする
            for colum in self.colum_detail:
                if colum[0] not in item_list:
                    item_list[colum[0]] = None
                data.append(item_list[colum[0]])
            data_sql = ', '.join(data)
            datas.append(data_sql)
        
        placeholders = ', '.join(['?'] * (len(self.column_detail)+2))
        insert_table_sql = f"INSERT INTO {self.table_name} VALUES ({placeholders})"
        cor.executemany(insert_table_sql,datas)
        conn.commit()

    def destroy_record_id(self,conn :Connection,condition,id :int):
        cor = conn.cursor()
        cor.execute(f"DELETE FROM {self.table_name} WHERE id={condition}")
        conn.commit()

    def destroy_record(self,conn :Connection,condition):
        cor = conn.cursor()
        cor.execute(f"DELETE FROM {self.table_name} WHERE {condition}")
        conn.commit()

    def destroy_all_record(self,conn :Connection):
        cor = conn.cursor()
        cor.execute(f"DELETE FROM {self.table_name}")
        conn.commit()
    
    def select_table(self,conn :Connection, condition):
        cor = conn.cursor()
        cor.execute(f"SELECT * FROM {self.table_name} WHERE {condition}")
        rows = cor.fetchall()
        return rows
    
    def select_all_table(self,conn :Connection):
        cor = conn.cursor()
        cor.execute(f"SELECT * FROM {self.table_name}")
        rows = cor.fetchall()
        return rows

    # TODO colum_detailに型があるので変更点の型のチェックを入れる
    def update_table(self,conn :Connection,  condition, update_item_list):
        cor = conn.cursor()
        update_colum = ", ".join([f"{key}=?" for key in update_item_list.keys()])
        cor.execute(f"UPDATE {self.table_name} SET {update_colum} WHERE {condition}", list(update_item_list.values()))
        conn.commit()

    def __del__(self):
        self.conn.close()
        print("Connection closed")


