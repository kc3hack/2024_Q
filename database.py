import sqlite3
from sqlite3 import Connection, Error

class table():
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

        return conn

    def close_connection(conn):
        conn.close()

    def create_table(self,conn, table_name, column_list):
        cor = conn.cursor()
        # CREATE TABLE文の基本形を作成
        create_table_sql = "CREATE TABLE " + table_name + " (id INTEGER PRIMARY KEY AUTOINCREMENT"
        
        # 辞書からカラム名とデータ型を取得してSQL文に追加
        # columns_sql = ', '.join([f"{column_name} {data_type}" for column_name, data_type in column_list.items()])
        # SQLite の 柔軟な型付け(flexible typing)機能のおかげで、データ型の指定はオプションになっています。(公式ドキュメント曰く)
        # なのでdatatypeをカット
        columns_sql = ""
        for colum_name,data_type in column_list.items():
            colums_sql += "," + data_type
            self.colum_detail.append([colum_name,data_type])
        # カラム定義をSQL文に追加し、最終的なSQL文を完成させる
        create_table_sql += columns_sql + ")"
        try:
            # SQL文を実行
            cor.execute(create_table_sql)
            print("Table created successfully")
        except Exception as e:
            print(f"An error occurred: {e}")

    def insert_table(conn :Connection, table_name, item_list:dict):
        column_list = item_list.keys()  # 辞書のキーを列名として取得

        columns = ', '.join(column_list)
        placeholders = ', '.join(['?'] * len(column_list))
        insert_table_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        conn.executemany(insert_table_sql,)




