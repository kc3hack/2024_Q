from datetime import timedelta
import dotenv
from flask import Flask

app = Flask(__name__)

app.secret_key = dotenv.get('SECRET_KEY')
app.permanent_session_lifetime = timedelta(minutes=5)