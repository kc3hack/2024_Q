from datetime import timedelta
import os
import dotenv
from flask import Flask

app = Flask(__name__)

dotenv.load_dotenv()
app.secret_key = os.environ["SECRET_KEY"]
app.permanent_session_lifetime = timedelta(minutes=5)