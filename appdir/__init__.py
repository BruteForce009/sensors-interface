import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '__RANDOM_KEY__'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


def split_func(strn):
    t = f'{strn}'
    return t.split()


def strip_func(strn):
    return strn.strip('SensorTypes')


app.jinja_env.globals.update(split_func=split_func)
app.jinja_env.globals.update(strip_func=strip_func)

from appdir import routes
