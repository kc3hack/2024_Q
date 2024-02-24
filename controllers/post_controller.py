from common.models.post import Posts
from flask import *
#画像投稿
import os
from werkzeug.utils import secure_filename
from common.models.user import User
from controllers.user_controller import user_controller
from common.models.store import Stores
app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class post_controller():
    def __init__(self) -> None:
        self.posts = Posts()
        self.stores = Stores()

    def read_all(self):
        #あとでformの名前かえる
        # sort = request.form['sort']
        post_list = self.posts.get_all_posts()
        # if(sort != None):
        #     post_list = self.posts.get_posts(f"title colum Link '%{sort}%'")
        user_list = []
        for post in post_list:
            user = User()
            user_info = user.get_user_info(post[4])
            user_list.append(user_info)
        posts_users = zip(post_list, user_list)
        return render_template('post/timeline.html',posts_users = posts_users)
    
    def read_post(self,id):
        post = self.posts.get_post(id)
        return render_template('post/detail.html',post = post)

    def create(self,user_id):
        if request.method == 'POST':
            title = request.form['title']
            place_id = request.form['placeId']
            body = request.form['comment']
            price = request.form['price']
            if not title:
                flash('商品名を記載してください')
                return render_template('post/create.html')
            if not place_id:
                flash('場所を記載してください')
                return render_template('post/create.html')
            if not body:
                flash('商品説明を記載してください')
                return render_template('post/create.html')
            if not price:
                flash('価格を記載してください')
                return render_template('post/create.html')
            
            # storeテーブルから取得したidを入れる
            tmp = self.stores.get_store_by_place_id(request.form['placeId'])
            if tmp:
                store_id = tmp[0][0]
            else:
                store_id = self.stores.create_store(request.form['placeId'])
            # error = None
        # #画像付き
        # if 'file' not in request.files:
        #     error = 'Image is required'
        # if error is not None:
        #     flash(error)
        # else:
        #     #画像付き
        #     file = request.files['file']
        #     if file.filename == '':
        #         return redirect(request.url)
        #     if file:
        #         filename = secure_filename(file.filename)
        #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #引数の追加
            self.posts.create_post(title,price,body,user_id,store_id)
            # self.posts.create_post(body,user_id)
            user = User()
            user_info = user.get_user_info(user_id)
            store_name = self.stores.get_store(store_id)[1]
            return render_template('post/show.html',title=title,price=price,body=body,store_name=store_name,user_info=user_info)
        return render_template('post/create.html')

        
    def delete(self,id):
        post = self.posts.get_post(id)
        if post is None:
            return render_template('error/404.html')
        elif post[3] != id:
            return render_template('error/403.html')
        self.posts.delete_post(id)
        return redirect(url_for('index'))
    
    def get_near_post(self, current_lat, current_lng):
        stores = self.stores.get_near_stores(current_lat, current_lng)
        
        posts = []
        for store in stores:
            store_id = store[0]
            store_posts = self.posts.get_posts(f"store_id={store_id}")
            posts.extend(store_posts)
            if len(posts) > 100:
                break

        return posts