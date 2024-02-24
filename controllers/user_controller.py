import flask
from flask import *
import dotenv


from common.models.user import User
app = flask.Flask(__name__)
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)

class user_controller():
    def __init__(self) -> None:
        self.user = User()
    def login(self):
        data = flask.request.form
        password = data['password']
        email = data['email']
        user_info = self.user.get_user_info_by_email(email)
        if self.user.password_check(user_info['id'],password):
            if user_info['state'] == 2:
                return flask.redirect('/error/401')
            # flask_login.login_user(user_info)
            session['user_id'] = user_info['id']
            session['user_name'] = user_info['userName']
            return flask.redirect('/') # TODO: ログイン後のリダイレクト先を指定
        else:
            return flask.redirect('/') #TODO: ログイン失敗時のレンだー先を指定

    def logout(self):
        session.pop('user_id',None)
        session.pop('user_name',None)
        return flask.redirect('/')
    
    # TODO emailの重複チェック
    def signup(self):
        data = flask.request.form
        print(data)
        
        self.user.create_user(data['name'],data['email'],data['password'],0)
        return flask.redirect('/user/login')#一旦/で
    
    # これどうしよう sessionから現在のログインユーザーとみたいユーザーのページが同じならこのメソッドみたいにしたいけど
    def currrent_user_info(self):
        
        user_info = self.user.get_user_info(session['user_id'])
        return user_info # TODO リダイレクトに変更
    
    def user_info(self,user_id):
        user = User()
        user_info = user.get_user_info(user_id)

     
        return flask.render_template('user/show.html',user_info=user_info)

    
    def user_delete(self):
        
        self.user.delete_user(session['user_id'])
        return flask.redirect('/logout')
    
    def user_update(self):
       
        self.user.update_user(session['user_id'])
        return flask.redirect(f'/user/{session["user_id"]}')
    
    def user_login_check(self):
        if 'user_id' in session:
            return True
        else:
            return False