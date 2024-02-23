from common.models.post import Posts
from flask import *
class post_controller():
    def __init__(self) -> None:
        self.posts = Posts()

    def read_all(self,condition):
        #あとでformの名前かえる
        sort = request.form['sort']
        post_list = self.posts.get_posts(condition)
        # if(sort != None):
        #     post_list = self.posts.get_posts(f"title colum Link '%{sort}%'")

        return render_template('timeline.html',post_list=post_list)
    
    def read_post(self,id):
        post = self.posts.get_post(id)
        return render_template('detail.html',post = post) 
      
    def create(self,user_id):
        if request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            self.posts.create_post(title,body,user_id)
            return redirect(url_for('index'))

        return render_template('post.html')
    
    def delete(self,id):
        post = self.posts.get_post(id)
        if post is None:
            return render_template('404.html')
        elif post[3] != id:
            return render_template('403.html')


        self.posts.delete_post(id)
        return redirect(url_for('index'))
    