import os
import dotenv
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
import requests
from common.models.store import Stores

from controllers.user_controller import user_controller
from controllers.post_controller import post_controller
app = Flask(__name__)
user_controller = user_controller()
post_controller = post_controller()
dotenv.load_dotenv()
app.secret_key = os.environ["SECRET_KEY"]


@app.route('/user/login', methods=['GET', 'POST'])
def login():
    if user_controller.user_login_check_flag():
        return redirect(url_for('index'))
    if request.method == 'POST':
        return user_controller.login()
    else:
        return render_template('user/login.html')
    
@app.route('/')
def index():
    if user_controller.user_login_check_flag():
       
        return render_template('index.html')
    return redirect(url_for('signup'))


# usercontrollerからのリターンがあるんだから、それをそのまま返せばいいのでは…？
# 後で考えます

@app.route('/user/logout', methods=['GET'])
def logout():
    return user_controller.logout()

@app.route('/user/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        return user_controller.signup()
    else:
        if user_controller.user_login_check_flag():
            return redirect(url_for('index'))
        return render_template('user/signup.html')

@app.route('/user/<int:user_id>', methods=['GET'])
def user_info(user_id):
    if user_controller.user_login_check_flag():
        if session['user_id'] == user_id:
            return user_controller.currrent_user_info()
        return user_controller.user_info(user_id)
    else:
        return redirect(url_for('login'))

@app.route('/user/update', methods=['GET', 'POST'])
def update_user():
    if not user_controller.user_login_check_flag():
        return redirect(url_for('login'))
    if request.method == 'POST':
        return user_controller.user_update()
    else:
        return render_template('user/update.html')

@app.route('/user/delete', methods=['GET'])
def delete_user():
    if not user_controller.user_login_check_flag():
        return redirect(url_for('login'))
    return user_controller.user_delete()

@app.route('/post/<int:post_id>', methods=['GET'])
def read_post(post_id):
    if not user_controller.user_login_check_flag():
        return redirect(url_for('login'))
    return post_controller.read_post(post_id)

@app.route('/post/index', methods=['GET'])
def read_all_post():
    if not user_controller.user_login_check_flag():
        return redirect(url_for('login'))
    return post_controller.read_all()

@app.route('/post/create', methods=['GET', 'POST'])
def create_post():
    if not user_controller.user_login_check_flag():
        return redirect(url_for('login'))
    if request.method == 'POST':
        return post_controller.create(session['user_id'])
    else:
        return render_template('post/create.html')

@app.route('/post/delete/<int:post_id>', methods=['GET'])
def delete_post(post_id):
    if not user_controller.user_login_check_flag():
        return redirect(url_for('login'))
    return post_controller.delete(post_id)

# これいる？
@app.route('/post/update/<int:post_id>', methods=['GET', 'POST'])
def update_post(post_id):
    if not user_controller.user_login_check_flag():
        return redirect(url_for('login'))
    if request.method == 'POST':
        return post_controller.update(post_id)
    else:
        return render_template('post/update.html')
    
@app.route('/post/search', methods=['GET'])
def search_post():
    if not user_controller.user_login_check_flag():
        return redirect(url_for('login'))
    return post_controller.read_all('state=1')

@app.errorhandler(404)
def error_404(error):
    return render_template('error/404.html')

@app.errorhandler(401)
def error_401(error):
    return render_template('error/401.html')

@app.errorhandler(500)
def error_500(error):
    return render_template('error/500.html')

# googleのapiを呼び出すやつ
@app.route('/api/places', methods=['GET'])
def get_places():
    # クライアントからのリクエストURLを取得
    url = request.args.get('url')
    url = url+"&key=AIzaSyATFKf-BmfXyh2H_QSjwXSLJZiAwp0cezw"
    # Google Places APIへのリクエストを送信
    response = requests.get(url)
    
    # APIからのレスポンスをJSON形式でクライアントに返す
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "API request failed"}), response.status_code

@app.route('/api/near_store', methods=['GET'])
def near_store():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    store = Stores()
    stores_info = store.get_near_stores(lat, lng)
    print(stores_info)
    ret = jsonify(stores_info)
    print(ret)
    return ret

@app.route('/api/search', methods=['GET'])
def search():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    return post_controller.get_near_post(lat,lng)



if __name__ == ('__main__'):
    app.run(debug=True, port=5050)

