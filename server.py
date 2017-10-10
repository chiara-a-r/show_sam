from flask import Flask
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

app = Flask(__name__)

app.config["SECRET_KEY"] = "Highly secret key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

engine = create_engine('sqlite:///SurveySystem.db')
Base=declarative_base()

