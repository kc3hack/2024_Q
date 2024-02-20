from flask import *
import argparse
import datetime
import netifaces

app = Flask(__name__)
UPLOAD_FOLDER = './static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

PAGE_FOLDER = './page/'

def read_file(file):
    html = open(PAGE_FOLDER+file,"r", encoding="utf-8")
    html_main = html.read()
    html.close()
    return html_main

@app.errorhandler(404)
def error_404(error):
    return read_file("error/404.html")

@app.errorhandler(401)
def error_401(error):
    return read_file("error/401.html")

@app.errorhandler(500)
def error_500(error):
    return read_file("error/500.html")

@app.route('/', methods=['GET', 'POST'])
def index():
    return read_file("index.html")

@app.route('/search', methods=['GET', 'POST'])
def search1():
    return read_file("search/index.html")

@app.route('/search/<string:word>', methods=['GET', 'POST'])
def search2(word=""):
    return read_file("search/index.html")

@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    return read_file("timeline/index.html")

@app.route('/post/<string:user>/<string:word>/', methods=['POST'])
def post1(user,word):
    if request.method == 'POST':
        return read_file(request)
    return read_file("post/index.html")

@app.route('/post', methods=['GET'])
def post2():
    return read_file("post/index.html")

@app.route('/mypage/<string:userid>', methods=['GET', 'POST'])
def mypage(userid=""):
    if userid == "":
        return read_file("error/404.html")
    else:
        return read_file("mypage/index.html")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--port', default="80")
    args = parser.parse_args()
    PORT = int(args.port)
    dt_now = datetime.datetime.now()
    addres_url = "http://"+netifaces.ifaddresses('en0')[netifaces.AF_INET][0]['addr']+":"+str(PORT)
    print(addres_url)
    app.run(host='0.0.0.0', port=PORT)