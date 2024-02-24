import sqlite3
from sqlite3 import Connection, Error

# TODO コードをきれいに、あとコメントも
# TODO 例外処理を入れる
# TODO 動作確認
# TODO sqlインジェクション対策

class Table():
    def __init__(self):
        self.column_detail = []
        self.table_name = ""

    def create_connection(self,db_file):
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
                self.column_detail.append([info[1][i],info[2][i]])


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
            for column_name,data_type in column_list.items():
                columns_sql += "," + column_name
                self.column_detail.append([column_name,data_type])
            # カラム定義をSQL文に追加し、最終的なSQL文を完成させる (,忘れてた)
            create_table_sql += columns_sql + ",created_at DEFAULT (DATETIME('now','localtime')) )"
            try:
                # SQL文を実行
                cor.execute(create_table_sql)
                # インスタンス変数にテーブル名をセット(忘れてた)
                self.table_name = table_name
                print("Table created successfully")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        else:
            print("Table already exists")

    # TODO column_detailに型があるので型のチェックを入れる
    def insert_table(self,conn :Connection, item_lists :list):
        cor = conn.cursor()

        datas = []
        try :
                # item_listの中身を取り出して、SQL文に埋め込める形にする
            for item_list in item_lists:
                data=[]
                # item_listの中身を取り出して、SQL文に埋め込める形にする
                for column in self.column_detail:
                    if column[0] not in item_list:
                        item_list[column[0]] = None
                    # joinは文字列しか受け付けないので文字列にするためにstrに変換
                    if type(item_list[column[0]]) != str:
                        data.append(str(item_list[column[0]]))
                    else:
                        data.append(item_list[column[0]])
                    # print(item_list[column[0]])
                    # print("column[0]")
                # data_sql = ','.join(data)
                datas.append(data)
            # 絡む情報の取得
            insert_columns = ','.join([column[0] for column in self.column_detail])

            placeholders = ','.join(['?'] * (len(self.column_detail)))
            # カラムの指定の追加
            insert_table_sql = f"INSERT INTO {self.table_name}({insert_columns}) VALUES ({placeholders})"
            # print(insert_table_sql)
            # print(datas)

            cor.executemany(insert_table_sql,datas)
            conn.commit()
        except Exception as e:
            print(e)
        else:
            print(insert_table_sql+datas+"多分正常に保存されたよ")

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
        print(f"DELETE FROM {self.table_name}")
        cor.execute(f"DELETE FROM {self.table_name}")
        print(f"DROP TABLE IF EXISTS {self.table_name}")
        cor.execute(f"DROP TABLE IF EXISTS {self.table_name}")

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

    # TODO column_detailに型があるので変更点の型のチェックを入れる
    def update_table(self,conn :Connection,  condition, update_item_list):
        cor = conn.cursor()
        update_column = ",".join([f"{key}=?" for key in update_item_list.keys()])
        cor.execute(f"UPDATE {self.table_name} SET {update_column} WHERE {condition}", list(update_item_list.values()))
        conn.commit()

    # def __del__(self):
    #     self.conn.close()
    #     print("Connection closed")
        
    def table_reset(self,conn :Connection):
        cor = conn.cursor()
        cor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        info = cor.fetchall()
        for table in info:
            if table[0] != "sqlite_sequence":
                print(f"DROP TABLE {table[0]}")
                cor.execute(f"DROP TABLE {table[0]}")
        conn.commit()
        print("Table reset")

    def get_column(self,conn :Connection):
        cor = conn.cursor()
        cor.execute(f"PRAGMA table_info({self.table_name})")
        rows = cor.fetchall()
        return rows

    def get_table(self,conn :Connection):
        cor = conn.cursor()
        cor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        info = cor.fetchall()
        tables = []
        for table in info:
            tables.append(table[0])
        return tables

