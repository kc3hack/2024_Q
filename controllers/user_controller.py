import flask
import flask_login
import dotenv
from common.models.user import User
app = flask.Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
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
            flask_login.login_user(user_info)
            return flask.redirect('/')
        else:
            return flask.redirect('/login')
