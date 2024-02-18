import sqlite3
from sqlite3 import Connection, Error

# TODO コードをきれいに、あとコメントも
# TODO    インスタンス変数を使え！
# TODO 例外処理を入れる
# TODO 動作確認
# TODO sqlインジェクション対策

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

    # TODO colum_detailに型があるので型のチェックを入れる
    def insert_table(self,conn :Connection, table_name, item_lists :list):
        cor = conn.cursor()
        # for colum in self.colum_detail:
        #     if colum[0] not in item_list:
        #         item_list[colum[0]] = None
        #     data.append(item_list[colum[0]])
        # data_sql = ', '.join(data)
        # datas.append(data_sql)

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
        
        # columns = ', '.join(column_list)
        placeholders = ', '.join(['?'] * len(self.column_detail))
        insert_table_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        cor.executemany(insert_table_sql,datas)
        conn.commit()

    def destroy_record_id(self,conn :Connection, table_name, condition,id :int):
        cor = conn.cursor()
        cor.execute(f"DELETE FROM {table_name} WHERE id={condition}")
        conn.commit()

    def destroy_record(self,conn :Connection, table_name):
        cor = conn.cursor()
        cor.execute(f"DELETE FROM {table_name}")
        conn.commit()
    
    def select_table(self,conn :Connection, table_name, condition):
        cor = conn.cursor()
        cor.execute(f"SELECT * FROM {table_name} WHERE {condition}")
        rows = cor.fetchall()
        return rows
    
    def select_all_table(self,conn :Connection, table_name):
        cor = conn.cursor()
        cor.execute(f"SELECT * FROM {table_name}")
        rows = cor.fetchall()
        return rows

    # TODO colum_detailに型があるので変更点の型のチェックを入れる
    def update_table(self,conn :Connection, table_name, condition, update_item_list):
        cor = conn.cursor()
        update_colum = ", ".join([f"{key}=?" for key in update_item_list.keys()])
        cor.execute(f"UPDATE {table_name} SET {update_colum} WHERE {condition}", list(update_item_list.values()))
        conn.commit()


