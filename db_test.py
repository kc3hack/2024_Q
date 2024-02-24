from db.database import Table
table = Table()
class Test():
    table_name = 'test'
    def __init__(self) -> None:
        self.table = Table()
        self.column_list = {
            "table1":"TEXT",
            "table2":"TEXT",
            "test_id":"INTEGER",
            "state":"INTEGER"
        }
        
        
        print('new')
    
        self.conn = table.create_connection('test_data.db')
        print('connect')
        # テーブルを作成する前にすべてのレコードを削除する
        self.table.table_reset(self.conn)
        self.table.create_table(self.conn,Test.table_name,self.column_list)
        print('create')

    def check_test(self,tablename):
        print(self.table.check_table(self.conn,tablename))

    def insert_test(self,table1,table2,id,state):
        item_list ={
            'table1':table1,
            'table2':table2,
            'test_id':id,
            'state':state
        }
        item_list2 ={
            'table1':table1,
            'table2':table2,
            'test_id':id,
            'state':state
        }
        item_lists = []
        item_lists.append(item_list)
        item_lists.append(item_list2)
        self.table.insert_table(self.conn,item_lists)
        print('insert')
    
    def select_all_test(self):
        print(self.table.select_all_table(self.conn))
    
    # テーブルクラスが管理するテーブルの削除
    def table_reset(self):
        self.table.destroy_all_record(self.conn)
        print('reset')

    # データベース上の削除できるテーブルの全削除
    def db_reset(self):
        self.table.table_reset(self.conn)
        print('all reset')
    
    # テーブルクラスが管理するテーブルの情報の取得
    def check_column(self):
        print("column:")
        info = self.table.get_column(self.conn)
        for i in info:
            print(i[1])
        print()

    def update_test(self,id):
        condition =  f'id={id}'
        self.table.update_table(self.conn,condition,{'state':2})
        print('update')
    
    # def get_table_test(self):
    #     table = self.table.get_table(self.conn)
    #     print(table)


    

test = Test()
# test.db_reset()
# test.check_test('test')
# test.check_test('fake')
# test.check_column()
test.insert_test('test11','test12',1,1)
test.select_all_test()
test.update_test(1)
test.select_all_test()
# test.get_table_test()
# test.db_reset()
# test.get_table_test()

# test.check_column()

