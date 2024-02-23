from db.database import Table

class Stores():
    table_name = "store"
    def __init__(self) -> None:
        self.table = Table()
        self.column_list = {
            "name":"TEXT",
            "lat":"REAL",
            "lng":"REAL",
            "user_id":"INTEGER",
            "state":"INTEGER",
            "created_at":"INTEGER"
        }
        self.conn = self.table.create_connection('sns_data.db')
        # あれここcreated_atのデフォルト値いらないのでは…？(database.pyですでに設定している)
        # それほかのテーブルでも同じこと言えますたぶん
        # あとでちょうせいする
        self.table.create_table(self.conn,Stores.table_name,self.column_list)

    def create_store(self,name,lat,lng,user_id):
        item_list = {
            'name':name,
            'lat':lat,
            'lng':lng,
            'user_id':user_id,
            'state':0
        }
        item_lists = []
        item_lists.append(item_list)
        self.table.insert_table(self.conn,item_lists)

    def delete_store(self,id):
        condition =  f'id={id}'
        self.table.update_table(self.conn,condition,{'state':2})

    def get_store(self,id):
        rows = self.table.select_table(self.conn,f"id={id}")
        return rows
    
    def get_stores(self,condition):
        rows = self.table.select_table(self.conn,condition)
        return rows
    
    # TODO 処理を考える 多分カラムに緯度経度を追加して、その情報を元に近くの店を取得する感じがいいかも
    def get_near_stores(self,user_location):
        rows = self.table.select_table(self.conn)
        return rows