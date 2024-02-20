from db.database import Table

class Posts():
    table_name = "post"
    def __init__(self) -> None:
        self.table = Table()
        self.column_list = {
            "title":"TEXT",
            "body":"TEXT",
            "user_id":"INTEGER",
            "state":"INTEGER"
        }
        self.conn = self.table.create_connection()
        self.table.create_table(self.conn,Posts.table_name,self.column_list)

    def create_post(self,title,body,user_id):
        item_list = {
            'title':title,
            'body':body,
            'user_id':user_id,
            'state':0
        }
        item_lists = []
        item_lists.append(item_list)
        self.table.insert_table(self.conn,item_lists)
    
    def delete_post(self,id):
        self.table.destroy_record_id(self.conn,id)
    
    def delete_user_post(self,user_id):
        self.table.destroy_record(self.conn,f"user_id={user_id}")
    
    def get_post(self,id):
        rows = self.table.select_table(self.conn,f"id={id}")
        return rows
    
    def get_posts(self,condition):
        rows = self.table.select_table(self.conn,condition)
        return rows

    def get_user_posts(self,user_id):
        rows = self.table.select_table(self.conn,f"user_id={user_id}")
        return rows