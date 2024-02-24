from db.database import Table

class Posts():
    table_name = "post"
    def __init__(self) -> None:
        self.table = Table()
        # 個数入れたほうがいいか…？
        # 個数を入れる場合priceはそのままでいい気がするけど入れなかった場合1つあたりの値段にした方が扱いやすいかもという気持ちがある
        self.column_list = {
            "title":"TEXT",
            "price":"INTEGER",
            "body":"TEXT",
            "user_id":"INTEGER",
            #imageをここでかんりする場合
            # "image_filename":"TEXT"
            "store_id":"INTEGER",
            "state":"INTEGER",
        }
        self.conn = self.table.create_connection('sns_data.db')
        self.table.create_table(self.conn,Posts.table_name,self.column_list)
        #引数も追加

    # def create_post(self,title,body,user_id,store_id,image_filename):
    def create_post(self,title,price,body,user_id,store_id):
        item_list = {
            'title':title,
            'price':price,
            'body':body,
            'user_id':user_id,
            #ここも変更
            # 'image_filename':image_filename,
            'store_id':store_id,
            'state':0
        }
        item_lists = []
        item_lists.append(item_list)
        self.table.set_table(self.conn,Posts.table_name)
        self.table.insert_table(self.conn,item_lists)
    
    def delete_post(self,id):
        self.table.set_table(self.conn,Posts.table_name)
        self.table.destroy_record_id(self.conn,id)
    
    def delete_user_post(self,user_id):
        self.table.set_table(self.conn,Posts.table_name)
        self.table.destroy_record(self.conn,f"user_id={user_id}")
    
    def get_post(self,id):
        self.table.set_table(self.conn,Posts.table_name)
        rows = self.table.select_table(self.conn,f"id={id}")
        return rows
    
    def get_posts(self,condition):
        self.table.set_table(self.conn,Posts.table_name)
        rows = self.table.select_table(self.conn,condition)
        return rows

    def get_user_posts(self,user_id):
        self.table.set_table(self.conn,Posts.table_name)
        rows = self.table.select_table(self.conn,f"user_id={user_id}")
        return rows