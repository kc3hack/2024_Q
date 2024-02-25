import requests
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
            "place_id":"TEXT",
            "state":"INTEGER",
        }
        self.conn = self.table.create_connection('sns_data.db')
        # あれここcreated_atのデフォルト値いらないのでは…？(database.pyですでに設定している)
        # それほかのテーブルでも同じこと言えますたぶん
        # あとでちょうせいする
        
        self.table.create_table(self.conn,Stores.table_name,self.column_list)
        # self.table.set_table(self.conn,Stores.table_name)
        # self.table.destroy_all_record(self.conn)

    # def create_store(self,place_id):
    #     # ここでgoogle places apiを呼び出して店舗情報を取得する
    #     # その情報を使って店舗を作成する
    #     name =
    #     lat =
    #     lng =
    #     item_list = {
    #         'name':name,
    #         'lat':lat,
    #         'lng':lng,
    #         'place_id':place_id,
    #         'state':0
    #     }
    #     item_lists = []
    #     item_lists.append(item_list)
    #     self.table.set_table(self.conn,Stores.table_name)
    #     self.table.insert_table(self.conn,item_lists)
    def create_store(self, place_id):
        # Google Places APIのエンドポイント
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        # Google Places APIキー。実際のキーに置き換えてください。
        api_key = "AIzaSyATFKf-BmfXyh2H_QSjwXSLJZiAwp0cezw"
        
        # APIリクエストのパラメータ
        params = {
            'place_id': place_id,
            'key': api_key,
            'fields': 'name,geometry/location'
        }
        
        # APIリクエストを送信
        response = requests.get(endpoint_url, params=params)
        
        # レスポンスから店舗情報を取得
        store_data = response.json()
        
        if store_data.get("status") == "OK":
            # 必要な店舗情報を取得
            result = store_data["result"]
            name = result["name"]
            lat = result["geometry"]["location"]["lat"]
            lng = result["geometry"]["location"]["lng"]
            
            # 店舗情報をデータベースに保存するためのリストを作成
            item_list = {
                'name': name,
                'lat': lat,
                'lng': lng,
                'place_id': place_id,
                'state': 0
            }
            item_lists = [item_list]
            
            # テーブル設定とデータ挿入
            self.table.set_table(self.conn, Stores.table_name)
            self.table.insert_table(self.conn, item_lists)
            store_id = self.table.select_table(self.conn, f"place_id='{place_id}'")[0][0]
            print('store_id  :')
            print(store_id)
            return store_id
        else:
            print("Failed to get store information from Google Places API.")

    def delete_store(self,id):
        condition =  f'id={id}'
        self.table.set_table(self.conn,Stores.table_name)
        self.table.update_table(self.conn,condition,{'state':2})

    def get_store(self,id):
        self.table.set_table(self.conn,Stores.table_name)
        rows = self.table.select_table(self.conn,f"id={id}")
        if not rows:
            return None
        return rows[0]
    
    def get_stores(self,condition=""):
        self.table.set_table(self.conn,Stores.table_name)
        rows = self.table.select_table(self.conn,condition)
        if not rows:
            return None
        return rows

    def get_store_by_place_id(self,place_id):
        self.table.set_table(self.conn,Stores.table_name)
        rows = self.table.select_table(self.conn,f"place_id='{place_id}'")
        return rows

    def haversine(self,lat1, lon1, lat2, lon2):
        R = 6371  # 地球の半径(km)
        
        phi1 = math.radians(float(lat1))
        phi2 = math.radians(float(lat2))
        delta_phi = math.radians(float(lat2) - float(lat1))
        delta_lambda = math.radians(float(lon2) - float(lon1))
        
        a = math.sin(delta_phi/2.0) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2.0) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        distance = R * c
        return distance

    def get_near_stores(self, current_lat, current_lng):
        # stores = self.get_stores("state=0")
        stores = self.get_stores()
        distances = []
        print(stores)
        for store in stores:
            store_lat = store[2]  # 緯度のカラムインデックスを指定
            store_lng = store[3]  # 経度のカラムインデックスを指定
            distance = self.haversine(current_lat, current_lng, store_lat, store_lng)
            distances.append((store, distance))
        
        # 距離でソート
        distances.sort(key=lambda x: x[1])

        # ソートされた店舗のリストを返す
        return distances