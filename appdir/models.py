from datetime import datetime
from appdir import db, login_manager
from flask_login import UserMixin
import enum


def remove(string):
    return string.replace(" ", "|")


@login_manager.user_loader
def load_user(user_username):
    return User.query.get(user_username)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    profile_pic = db.Column(db.String(45), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    sensors = db.relationship('Sensor', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class SensorTypes(enum.Enum):
    TEMPERATURE = 'temperature'
    HUMIDITY = 'humidity'
    PRESSURE = 'pressure'
    LUMINOSITY = 'luminosity'


class Sensor(db.Model, UserMixin):
    model_no = db.Column(db.String(30), nullable=False, primary_key=True)
    type = db.Column(db.Enum(SensorTypes), nullable=False)
    desc = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float(precision=6), nullable=True)
    longitude = db.Column(db.Float(precision=6), nullable=True)
    value = db.Column(db.Float(precision=6), nullable=True)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"{self.model_no} {self.type} {self.latitude} {self.longitude} {self.value}"


class SensorData(db.Model):
    NodeID = db.Column(db.String(30), nullable=True, unique=False)
    pm1 = db.Column(db.Float(precision=2), nullable=True, unique=False)
    pm2 = db.Column(db.Float(precision=2), nullable=True, unique=False)
    pm3 = db.Column(db.Float(precision=2), nullable=True, unique=False)
    am = db.Column(db.Float(precision=2), nullable=True, unique=False)
    twd = db.Column(db.String(30), nullable=True, unique=False)
    sm1 = db.Column(db.Float(precision=2), nullable=True, unique=False)
    sm2 = db.Column(db.Float(precision=2), nullable=True, unique=False)
    st = db.Column(db.Float(precision=2), nullable=True, unique=False)
    lum = db.Column(db.Float(precision=2), nullable=True, unique=False)
    temp = db.Column(db.Float(precision=2), nullable=True, unique=False)
    humd = db.Column(db.Float(precision=2), nullable=True, unique=False)
    pres = db.Column(db.Float(precision=2), nullable=True, unique=False)
    bat = db.Column(db.Float(precision=2), nullable=True, unique=False)
    ttime = db.Column(db.String(30), primary_key=True, default=remove(f'{datetime.utcnow()}'))

    def __repr__(self):
        return f"{self.NodeID} {self.pm1} {self.pm2} {self.pm3} {self.am} {self.twd} {self.sm1} {self.sm2} {self.st} {self.lum} {self.temp} {self.humd} {self.pres} {self.bat} {self.ttime}"