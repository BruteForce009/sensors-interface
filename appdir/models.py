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

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class SensorDataUno(db.Model):
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


class SensorDataNrf(db.Model):
    NodeID = db.Column(db.String(30), nullable=True, unique=False)
    pm1 = db.Column(db.Float(precision=2), nullable=True, unique=False)
    pm2 = db.Column(db.Float(precision=2), nullable=True, unique=False)
    pm3 = db.Column(db.Float(precision=2), nullable=True, unique=False)
    am = db.Column(db.Float(precision=2), nullable=True, unique=False)
    twd = db.Column(db.String(30), nullable=True, unique=False)
    sm = db.Column(db.Float(precision=2), nullable=True, unique=False)
    st = db.Column(db.Float(precision=2), nullable=True, unique=False)
    lum = db.Column(db.Float(precision=2), nullable=True, unique=False)
    temp = db.Column(db.Float(precision=2), nullable=True, unique=False)
    humd = db.Column(db.Float(precision=2), nullable=True, unique=False)
    pres = db.Column(db.Float(precision=2), nullable=True, unique=False)
    bat = db.Column(db.Float(precision=2), nullable=True, unique=False)
    ttime = db.Column(db.String(30), primary_key=True, default=remove(f'{datetime.utcnow()}'))

    def __repr__(self):
        return f"{self.NodeID} {self.pm1} {self.pm2} {self.pm3} {self.am} {self.twd} {self.sm} {self.st} {self.lum} {self.temp} {self.humd} {self.pres} {self.bat} {self.ttime}"


class SensorData(db.Model):
    NodeID = db.Column(db.String(30), nullable=True, unique=False)
    pm1 = db.Column(db.Float(precision=2), nullable=True, unique=False)
    pm2 = db.Column(db.Float(precision=2), nullable=True, unique=False)
    pm3 = db.Column(db.Float(precision=2), nullable=True, unique=False)
    am = db.Column(db.Float(precision=2), nullable=True, unique=False)
    twd = db.Column(db.String(30), nullable=True, unique=False)
    sm = db.Column(db.Float(precision=2), nullable=True, unique=False)
    st = db.Column(db.Float(precision=2), nullable=True, unique=False)
    lum = db.Column(db.Float(precision=2), nullable=True, unique=False)
    temp = db.Column(db.Float(precision=2), nullable=True, unique=False)
    humd = db.Column(db.Float(precision=2), nullable=True, unique=False)
    pres = db.Column(db.Float(precision=2), nullable=True, unique=False)
    lat = db.Column(db.Float(precision=2), nullable=True, unique=False)
    NSI = db.Column(db.String(30), nullable=True, unique=False)
    long = db.Column(db.Float(precision=2), nullable=True, unique=False)
    EWI = db.Column(db.String(30), nullable=True, unique=False)
    alt = db.Column(db.Float(precision=2), nullable=True, unique=False)
    bat = db.Column(db.Float(precision=2), nullable=True, unique=False)
    ttime = db.Column(db.String(30), primary_key=True, default=remove(f'{datetime.utcnow()}'))
    rtctime = db.Column(db.Integer, nullable=True, unique=False, default=404)

    def __repr__(self):
        return f"{self.NodeID} {self.pm1} {self.pm2} {self.pm3} {self.am} {self.twd} {self.sm} {self.st} {self.lum} {self.temp} {self.humd} {self.pres} {self.lat} {self.NSI} {self.long} {self.EWI} {self.alt} {self.bat} {self.ttime}"