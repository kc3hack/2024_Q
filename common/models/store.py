from db.database import Table
import math

class Stores():
    table_name = "store"
    def __init__(self) -> None:
        self.table = Table()
        self.column_list = {
            "name":"TEXT",
            "lat":"REAL",
            "lng":"REAL",
            "plase_id":"INTEGER",
            "state":"INTEGER",
        }
        self.conn = self.table.create_connection('sns_data.db')
        # あれここcreated_atのデフォルト値いらないのでは…？(database.pyですでに設定している)
        # それほかのテーブルでも同じこと言えますたぶん
        # あとでちょうせいする
        self.table.create_table(self.conn,Stores.table_name,self.column_list)

    def create_store(self,name,lat,lng,place_id):
        item_list = {
            'name':name,
            'lat':lat,
            'lng':lng,
            'place_id':place_id,
            'state':0
        }
        item_lists = []
        item_lists.append(item_list)
        self.table.set_table(self.conn,Stores.table_name)
        self.table.insert_table(self.conn,item_lists)

    def delete_store(self,id):
        condition =  f'id={id}'
        self.table.set_table(self.conn,Stores.table_name)
        self.table.update_table(self.conn,condition,{'state':2})

    def get_store(self,id):
        self.table.set_table(self.conn,Stores.table_name)
        rows = self.table.select_table(self.conn,f"id={id}")
        return rows
    
    def get_stores(self,condition):
        self.table.set_table(self.conn,Stores.table_name)
        rows = self.table.select_table(self.conn,condition)
        return rows

    def get_store_by_place_id(self,place_id):
        self.table.set_table(self.conn,Stores.table_name)
        rows = self.table.select_table(self.conn,f"place_id={place_id}")
        return rows

    def haversine(self,lat1, lon1, lat2, lon2):
        R = 6371  # 地球の半径(km)
        
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        
        a = math.sin(delta_phi/2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2.0) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        distance = R * c
        return distance

    def get_near_stores(self, current_lat, current_lng):
        stores = self.get_stores("state=0")
        distances = []

        for store in stores:
            store_lat = store[2]  # 緯度のカラムインデックスを指定
            store_lng = store[3]  # 経度のカラムインデックスを指定
            distance = haversine(current_lat, current_lng, store_lat, store_lng)
            distances.append((store, distance))
        
        # 距離でソート
        distances.sort(key=lambda x: x[1])

        # ソートされた店舗のリストを返す
        return [store for store, distance in distances]