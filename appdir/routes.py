from flask import render_template, url_for, flash, redirect, get_flashed_messages, request
from appdir import app, db, bcrypt
import appdir.models
import appdir.forms
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from datetime import datetime
import os
import time
import math
import json
import secrets


def remove(string):
    return string.replace(" ", "|")


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = appdir.forms.LoginForm()
    if form.validate_on_submit():
        user = appdir.models.User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('login'))
        else:
            flash('Please enter correct email and password', 'danger')
            time.sleep(1)
            return render_template('fail.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = appdir.forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = appdir.models.User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        time.sleep(1)
        return render_template('success.html', title='Register', form=form)
    return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    pic_fn = random_hex + f_ext
    pic_path = os.path.join(app.root_path, 'static/images', pic_fn)

    output_size=(55, 65)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(pic_path)

    return pic_fn


@app.route("/jsondata", methods=['POST'])
def jsondata():
    request_data = request.get_json()

    NodeID = request_data['NodeID']
    pm1 = float(request_data['pm1'])
    pm2 = float(request_data['pm2'])
    pm3 = float(request_data['pm3'])
    am = float(request_data['am'])
    twd = request_data['twd']
    sm1 = float(request_data['sm1'])
    sm2 = float(request_data['sm2'])
    st = float(request_data['st'])
    lum = float(request_data['lum'])
    temp = float(request_data['temp'])
    humd = float(request_data['humd'])
    pres = float(request_data['pres'])
    bat = float(request_data['bat'])
    ttime = request_data['ttime']

    sensordata = appdir.models.SensorData(NodeID=NodeID, pm1=pm1, pm2=pm2, pm3=pm3, am=am, twd=twd, sm1=sm1, sm2=sm2, st=st, lum=lum, temp=temp, humd=humd, pres=pres, bat=bat, ttime=ttime)
    db.session.add(sensordata)
    db.session.commit()
    return 'Done'


@app.route("/newjsondata", methods=['POST'])
def newjsondata():
    request_data = request.get_json()
    ttime = remove(f'{datetime.utcnow()}')

    if request_data:
        if 'NodeID' in request_data:
            NodeID = request_data['NodeID']
        if 'pm1' in request_data:
            pm1 = float(request_data['pm1'])
        if 'pm2' in request_data:
            pm2 = float(request_data['pm2'])
        if 'pm3' in request_data:
            pm3 = float(request_data['pm3'])
        if 'am' in request_data:
            am = float(request_data['am'])
        if 'twd' in request_data:
            twd = request_data['twd']
        if 'sm1' in request_data:
            sm1 = float(request_data['sm1'])
        if 'sm2' in request_data:
            sm2 = float(request_data['sm2'])
        if 'st' in request_data:
            st = float(request_data['st'])
        if 'lum' in request_data:
            lum = float(request_data['lum'])
        if 'temp' in request_data:
            temp = float(request_data['temp'])
        if 'humd' in request_data:
            humd = float(request_data['humd'])
        if 'pres' in request_data:
            pres = float(request_data['pres'])
        if 'bat' in request_data:
            bat = float(request_data['bat'])
        if 'ttime' in request_data:
            ttime = request_data['ttime']

        sensordata = appdir.models.SensorData(NodeID=NodeID, pm1=pm1, pm2=pm2, pm3=pm3, am=am, twd=twd, sm1=sm1, sm2=sm2, st=st, lum=lum, temp=temp, humd=humd, pres=pres, bat=bat, ttime=ttime)
        db.session.add(sensordata)
        db.session.commit()
    return 'Done'


@app.route("/data_")
@login_required
def data_():
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    # form = appdir.forms.PictureForm()
    # if form.validate_on_submit():
    #     pic_file = save_pic(form.picture.data)
    #     current_user.profile_pic = pic_file
    page = request.args.get('page', 1, type=int)
    sensorL = appdir.models.SensorData.query.order_by(appdir.models.SensorData.ttime.desc()).paginate(page=page, per_page=9)
    ttl = math.floor(sensorL.total/9 + 1)
    return render_template('data_.html', sensorL=sensorL, ttl=ttl, img_file=img_file)


@app.route("/account")
@login_required
def account():
    img_file = url_for('static', filename='images/'+current_user.profile_pic)
    # form = appdir.forms.PictureForm()
    # if form.validate_on_submit():
    #     pic_file = save_pic(form.picture.data)
    #     current_user.profile_pic = pic_file
    sensor = appdir.models.Sensor.query.filter_by(owner=current_user.id).all()
    return render_template('account.html', sensor=sensor, img_file=img_file)


@app.route("/nrf5")
@login_required
def nrf5():
    img_file = url_for('static', filename='images/'+current_user.profile_pic)
    sensor = appdir.models.Sensor.query.filter_by(owner=current_user.id).all()
    return render_template('nrf5.html', sensor=sensor, img_file=img_file)


@app.route("/plot")
@login_required
def plot():
    img_file = url_for('static', filename='images/'+current_user.profile_pic)
    return render_template('plot.html', img_file=img_file)


@app.route("/nrf5_plot")
@login_required
def nrf5_plot():
    img_file = url_for('static', filename='images/'+current_user.profile_pic)
    return render_template('nrf5_plot.html', img_file=img_file)


@app.route("/data_plot")
@login_required
def data_plot():
    img_file = url_for('static', filename='images/'+current_user.profile_pic)
    return render_template('data_plot.html', img_file=img_file)
