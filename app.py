import os
import dotenv
from flask import Flask, redirect, render_template, request, url_for

from controllers.user_controller import user_controller
from controllers.post_controller import post_controller
app = Flask(__name__)
user_controller = user_controller()
post_controller = post_controller()
dotenv.load_dotenv()
app.secret_key = os.environ["SECRET_KEY"]


@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_controller.login()
    else:
        return render_template('user/login.html')
    
@app.route('/')
def index():
    return redirect(url_for('signup'))


# usercontrollerからのリターンがあるんだから、それをそのまま返せばいいのでは…？
# 後で考えます

@app.route('/user/logout', methods=['GET'])
def logout():
    return user_controller.logout()

@app.route('/user/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_controller.signup()
    else:
        return render_template('user/signup.html')
    
@app.route('/user/<int:user_id>', methods=['GET'])
def user_info(user_id):
    return user_controller.user_info(user_id)

@app.route('/user/update', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        return user_controller.user_update()
    else:
        return render_template('user/update.html')

@app.route('/user/delete', methods=['GET'])
def delete_user():
    return user_controller.user_delete()
@app.route('/post/<int:post_id>', methods=['GET'])
def read_post(post_id):
    return post_controller.read_post(post_id)

@app.route('/post/index', methods=['GET'])
def read_all_post():
    return post_controller.read_all()

@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        return post_controller.create()
    else:
        return render_template('post/create.html')

@app.route('/post/delete/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    return post_controller.delete(post_id)

@app.route('/post/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    if request.method == 'POST':
        return post_controller.update(post_id)
    else:
        return render_template('post/update.html')
    
@app.route('/post/search', methods=['GET'])
def search_post():
    return post_controller.search()

@app.errorhandler(404)
def error_404(error):
    return render_template('error/404.html')

@app.errorhandler(401)
def error_401(error):
    return render_template('error/401.html')

@app.errorhandler(500)
def error_500(error):
    return render_template('error/500.html')

if __name__ == ('__main__'):
    app.run(debug=True, port=5050)

