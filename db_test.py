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
        item_lists = []
        item_lists.append(item_list)
        self.table.insert_table(self.conn,item_lists)
        print('insert')
    
    # def select_all_test(self):
    #     print(self.table.select_all_table(self.conn))

test = Test()
test.check_test('test')
test.check_test('fake')
test.insert_test('test11','test12',1,1)
# test.select_all_test()