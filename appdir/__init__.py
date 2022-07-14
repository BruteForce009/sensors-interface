from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from appdir.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
mail = Mail(app)


def split_func(strn):
    t = f'{strn}'
    return t.split()


def strip_func(strn):
    return strn.strip('SensorTypes')


app.jinja_env.globals.update(split_func=split_func)
app.jinja_env.globals.update(strip_func=strip_func)

from appdir import routes
from appdir import handlers
