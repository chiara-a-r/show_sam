# This may be merged with the older server.py #
# By Wendy on 30 Sep #

from flask import Flask
from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY'] = 'Another_highly_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)