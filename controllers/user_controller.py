import flask
from flask import session
# import flask_login
import dotenv
from common.models.user import User
app = flask.Flask(__name__)
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)
app.secret_key = dotenv.get('SECRET_KEY')

class User_controller():
    def login():
        data = flask.request.form
        password = data['password']
        email = data['email']
        user = User()
        user_info = user.get_user_info_by_email(email)
        if user.password_check(user_info['id'],password):
            if user_info['state'] == 2:
                return flask.redirect('/error/401')
            # flask_login.login_user(user_info)
            session['user_id'] = user_info['id']
            session['user_name'] = user_info['userName']
            return flask.redirect('/') # TODO: ログイン後のリダイレクト先を指定
        else:
            return flask.redirect('/login') #TODO: ログイン失敗時のレンだー先を指定

    def logout():
        session.pop('user_id',None)
        session.pop('user_name',None)
        return flask.redirect('/')
    
    # TODO emailの重複チェック
    def signup():
        data = flask.request.form
        user = User()
        user.create_user(data['userName'],data['email'],data['password'],0)
        return flask.redirect('/login')
    
    def currrent_user_info():
        user = User()
        user_info = user.get_user_info(session['user_id'])
        return user_info # TODO リダイレクトに変更
    
    def user_info(user_id):
        user = User()
        user_info = user.get_user_info(user_id)
        return user_info # TODO リダイレクトに変更