from common.models.post import Posts
from flask import *
#画像投稿
import os
from werkzeug.utils import secure_filename

from common.models.store import Stores
app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class post_controller():
    def __init__(self) -> None:
        self.posts = Posts()
        self.stores = Stores()

    def read_all(self,condition):
        #あとでformの名前かえる
        sort = request.form['sort']
        post_list = self.posts.get_posts(condition)
        # if(sort != None):
        #     post_list = self.posts.get_posts(f"title colum Link '%{sort}%'")

        return render_template('post/timeline.html',post_list=post_list)
    
    def read_post(self,id):
        post = self.posts.get_post(id)
        return render_template('post/detail.html',post = post)

    def create(self,user_id):
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            price = request.form['price']
            # storeテーブルから取得したidを入れる
            store_id = self.stores.get_store_by_place_id(request.form['place_id'])[0]
            error = None

        if not title:
            error = 'Title is required.'
        # #画像付き
        # if 'file' not in request.files:
        #     error = 'Image is required'
        if error is not None:
            flash(error)
        # else:
        #     #画像付き
        #     file = request.files['file']
        #     if file.filename == '':
        #         return redirect(request.url)
        #     if file:
        #         filename = secure_filename(file.filename)
        #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #引数の追加
            # self.posts.create_post(title,body,user_id,filename)
            return redirect(url_for('index'))
        return render_template('post/post.html')

        
    def delete(self,id):
        post = self.posts.get_post(id)
        if post is None:
            return render_template('error/404.html')
        elif post[3] != id:
            return render_template('error/403.html')


        self.posts.delete_post(id)
        return redirect(url_for('index'))