from flask import render_template, url_for, flash, redirect, get_flashed_messages, request
from appdir import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from datetime import datetime
from PIL import Image
import appdir.models
import appdir.forms
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import time
import math
import json
import secrets


plt.rcParams['figure.figsize'] = [14, 5]


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


def remove(string):
    return string.replace(" ", "|")


def reformat(string):
    newstring = string.replace("|", "").replace(":", "").replace("-", "")
    return int(newstring)


@app.route('/', methods=['GET', 'POST'])
def lora():
    if request.method == 'POST':
        request_data = request.get_json()
        if request_data:
            file = open("jsondata.json", 'w')
            json.dump(request_data, file)
            file.close()
            return 'Done'
        else:
            return 'Not Done'
    file = open("jsondata.json", 'r')
    jdata = file.read()
    file.close()
    return render_template('lora.html', request_data=jdata)


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


@app.route("/jsondata", methods=['POST'])
def jsondata():
    request_data = request.get_json()

    NodeID = request_data['NodeID']
    pm1 = float(request_data['pm1'])
    pm2 = float(request_data['pm2'])
    pm3 = float(request_data['pm3'])
    am = float(request_data['am'])
    twd = request_data['twd']
    sm = float(request_data['sm'])
    st = float(request_data['st'])
    lum = float(request_data['lum'])
    temp = float(request_data['temp'])
    humd = float(request_data['humd'])
    pres = float(request_data['pres'])
    lat = float(request_data['lat'])
    NSI = request_data['NSI']
    long = float(request_data['long'])
    EWI = request_data['EWI']
    alt = float(request_data['alt'])
    bat = float(request_data['bat'])
    ttime = int(request_data['ttime'])

    rtctime = ttime
    new_time = datetime.fromtimestamp(ttime)
    ttime = remove(f'{new_time}')

    sensordata = appdir.models.SensorData(NodeID=NodeID, pm1=pm1, pm2=pm2, pm3=pm3, am=am, twd=twd, sm=sm, st=st, lum=lum, temp=temp, humd=humd, pres=pres, lat=lat, NSI=NSI, long=long, EWI=EWI, alt=alt, bat=bat, ttime=ttime, rtctime=rtctime)
    db.session.add(sensordata)
    db.session.commit()
    return 'Done'


@app.route("/newjsondata", methods=['POST'])
def newjsondata():
    request_data = request.get_json()

    NodeID = 'X'
    pm1 = 1.23
    pm2 = 1.23
    pm3 = 1.23
    am = 1.23
    twd = 'X'
    sm = 1.23
    st = 1.23
    lum = 1.23
    temp = 1.23
    humd = 1.23
    pres = 1.23
    lat = 1.23
    NSI = 'X'
    long = 1.23
    EWI = 'X'
    alt = 1.23
    bat = 1.23

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
        if 'sm' in request_data:
            sm = float(request_data['sm'])
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
        if 'lat' in request_data:
            lat = float(request_data['lat'])
        if 'NSI' in request_data:
            NSI = request_data['NSI']
        if 'long' in request_data:
            long = float(request_data['long'])
        if 'EWI' in request_data:
            EWI = request_data['EWI']
        if 'alt' in request_data:
            alt = float(request_data['alt'])
        if 'bat' in request_data:
            bat = float(request_data['bat'])
        if 'ttime' in request_data:
            ttime = int(request_data['ttime'])
            rtctime = ttime
            new_time = datetime.fromtimestamp(ttime)
            ttime = remove(f'{new_time}')
        else:
            ttime = remove(f'{datetime.utcnow()}')

        sensordata = appdir.models.SensorData(NodeID=NodeID, pm1=pm1, pm2=pm2, pm3=pm3, am=am, twd=twd, sm=sm, st=st, lum=lum, temp=temp, humd=humd, pres=pres, lat=lat, NSI=NSI, long=long, EWI=EWI, alt=alt, bat=bat, ttime=ttime, rtctime=rtctime)
        db.session.add(sensordata)
        db.session.commit()
    return 'Done'


@app.route("/unopost", methods=['POST'])
def unopost():
    request_data = request.get_json()

    NodeID = 'X'
    pm1 = 1.23
    pm2 = 1.23
    pm3 = 1.23
    am = 1.23
    twd = 'X'
    sm = 1.23
    st = 1.23
    lum = 1.23
    temp = 1.23
    humd = 1.23
    pres = 1.23
    lat = 1.23
    NSI = 'X'
    long = 1.23
    EWI = 'X'
    alt = 1.23
    bat = 1.23

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
        if 'sm' in request_data:
            sm = float(request_data['sm'])
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
        if 'lat' in request_data:
            lat = float(request_data['lat'])
        if 'NSI' in request_data:
            NSI = request_data['NSI']
        if 'long' in request_data:
            long = float(request_data['long'])
        if 'EWI' in request_data:
            EWI = request_data['EWI']
        if 'alt' in request_data:
            alt = float(request_data['alt'])
        if 'bat' in request_data:
            bat = float(request_data['bat'])
        if 'ttime' in request_data:
            ttime = int(request_data['ttime'])
            rtctime = ttime
            new_time = datetime.fromtimestamp(ttime)
            ttime = remove(f'{new_time}')
        else:
            ttime = remove(f'{datetime.utcnow()}')

        sensordata = appdir.models.SensorDataUno(NodeID=NodeID, pm1=pm1, pm2=pm2, pm3=pm3, am=am, twd=twd, sm=sm, st=st, lum=lum, temp=temp, humd=humd, pres=pres, lat=lat, NSI=NSI, long=long, EWI=EWI, alt=alt, bat=bat, ttime=ttime, rtctime=rtctime)
        db.session.add(sensordata)
        db.session.commit()
    return 'Done'


@app.route("/nrfpost", methods=['POST'])
def nrfpost():
    request_data = request.get_json()

    NodeID = 'X'
    pm1 = 1.23
    pm2 = 1.23
    pm3 = 1.23
    am = 1.23
    twd = 'X'
    sm = 1.23
    st = 1.23
    lum = 1.23
    temp = 1.23
    humd = 1.23
    pres = 1.23
    lat = 1.23
    NSI = 'X'
    long = 1.23
    EWI = 'X'
    alt = 1.23
    bat = 1.23

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
        if 'sm' in request_data:
            sm = float(request_data['sm'])
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
        if 'lat' in request_data:
            lat = float(request_data['lat'])
        if 'NSI' in request_data:
            NSI = request_data['NSI']
        if 'long' in request_data:
            long = float(request_data['long'])
        if 'EWI' in request_data:
            EWI = request_data['EWI']
        if 'alt' in request_data:
            alt = float(request_data['alt'])
        if 'bat' in request_data:
            bat = float(request_data['bat'])
        if 'ttime' in request_data:
            ttime = int(request_data['ttime'])
            rtctime = ttime
            new_time = datetime.fromtimestamp(ttime)
            ttime = remove(f'{new_time}')
        else:
            ttime = remove(f'{datetime.utcnow()}')

        sensordata = appdir.models.SensorDataNrf(NodeID=NodeID, pm1=pm1, pm2=pm2, pm3=pm3, am=am, twd=twd, sm=sm, st=st, lum=lum, temp=temp, humd=humd, pres=pres, lat=lat, NSI=NSI, long=long, EWI=EWI, alt=alt, bat=bat, ttime=ttime, rtctime=rtctime)
        db.session.add(sensordata)
        db.session.commit()
    return 'Done'


@app.route("/account")
@login_required
def account():
    img_file = url_for('static', filename='images/'+current_user.profile_pic)
    page = request.args.get('page', 1, type=int)
    sensorA = appdir.models.SensorDataUno.query.filter_by(NodeID=current_user.username).order_by(appdir.models.SensorDataUno.rtctime.desc()).paginate(page=page, per_page=9)
    ttl = math.floor(sensorA.total / 9 + 1)
    return render_template('account.html', sensorA=sensorA, ttl=ttl, img_file=img_file)


@app.route("/nrf5")
@login_required
def nrf5():
    img_file = url_for('static', filename='images/'+current_user.profile_pic)
    page = request.args.get('page', 1, type=int)
    sensorN = appdir.models.SensorDataNrf.query.filter_by(NodeID=current_user.username).order_by(appdir.models.SensorDataNrf.rtctime.desc()).paginate(page=page, per_page=9)
    ttl = math.floor(sensorN.total / 9 + 1)
    return render_template('nrf5.html', sensorN=sensorN, ttl=ttl, img_file=img_file)


@app.route("/data_")
@login_required
def data_():
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    page = request.args.get('page', 1, type=int)
    sensorL = appdir.models.SensorData.query.order_by(appdir.models.SensorData.rtctime.desc()).filter_by(NodeID=current_user.username).paginate(page=page, per_page=9)
    ttl = math.floor(sensorL.total/9 + 1)
    return render_template('data_.html', sensorL=sensorL, ttl=ttl, img_file=img_file)


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
    conn = db.engine.connect()
    df = pd.read_sql_table('sensor_data', conn)
    sorted = df.sort_values(by='rtctime', ascending=True)
    ttime = sorted['rtctime']
    pm1 = sorted['pm1']
    x_indexes = np.arange(len(ttime))
    plt.figure(1)
    plt.style.use('fivethirtyeight')
    plt.bar(x_indexes, pm1, label='pm1')
    plt.xlabel('Readings (288/day)')
    plt.ylabel('Rain in the current hour (mm)')
    plt.title('Pluviometer 1')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('appdir/static/images/pm1.png')
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    return render_template('data_plot.html', img_file=img_file)


@app.route("/pm2")
@login_required
def pm2():
    conn = db.engine.connect()
    df = pd.read_sql_table('sensor_data', conn)
    sorted = df.sort_values(by='rtctime', ascending=True)
    ttime = sorted['rtctime']
    pm2 = sorted['pm2']
    x_indexes = np.arange(len(ttime))
    plt.figure(2)
    plt.style.use('fivethirtyeight')
    plt.bar(x_indexes, pm2, label='pm2')
    plt.xlabel('Readings (288/day)')
    plt.ylabel('Rain in the previous hour (mm)')
    plt.title('Pluviometer 2')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('appdir/static/images/pm2.png')
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    return render_template('pm2.html', img_file=img_file)


@app.route("/pm3")
@login_required
def pm3():
    conn = db.engine.connect()
    df = pd.read_sql_table('sensor_data', conn)
    sorted = df.sort_values(by='rtctime', ascending=True)
    ttime = sorted['rtctime']
    pm3 = sorted['pm3']
    x_indexes = np.arange(len(ttime))
    plt.figure(3)
    plt.style.use('ggplot')
    plt.plot(x_indexes, pm3, label='pm3')
    plt.xlabel('Readings (288/day)')
    plt.ylabel('Rain in the last 24 hours (mm)')
    plt.title('Pluviometer 3')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('appdir/static/images/pm3.png')
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    return render_template('pm3.html', img_file=img_file)


@app.route("/anemo")
@login_required
def anemo():
    conn = db.engine.connect()
    df = pd.read_sql_table('sensor_data', conn)
    sorted = df.sort_values(by='rtctime', ascending=True)
    ttime = sorted['rtctime']
    am = sorted['am']
    x_indexes = np.arange(len(ttime))
    plt.figure(4)
    plt.style.use('fivethirtyeight')
    plt.bar(x_indexes, am, label='Anemometer')
    plt.xlabel('Readings (288/day)')
    plt.ylabel('Wind Speed (km/h)')
    plt.title('Anemometer')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('appdir/static/images/am.png')
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    return render_template('anemo.html', img_file=img_file)


@app.route("/sm")
@login_required
def sm():
    conn = db.engine.connect()
    df = pd.read_sql_table('sensor_data', conn)
    sorted = df.sort_values(by='rtctime', ascending=True)
    ttime = sorted['rtctime']
    sm = sorted['sm']
    x_indexes = np.arange(len(ttime))
    plt.figure(5)
    plt.style.use('fivethirtyeight')
    plt.bar(x_indexes, sm, label='Soil Moisture')
    plt.xlabel('Readings (288/day)')
    plt.ylabel('Soil moisture (centibar)')
    plt.title('Watermark')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('appdir/static/images/sm.png')
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    return render_template('sm.html', img_file=img_file)


@app.route("/st")
@login_required
def st():
    conn = db.engine.connect()
    df = pd.read_sql_table('sensor_data', conn)
    sorted = df.sort_values(by='rtctime', ascending=True)
    ttime = sorted['rtctime']
    st = sorted['st']
    x_indexes = np.arange(len(ttime))
    plt.figure(6)
    plt.style.use('fivethirtyeight')
    plt.bar(x_indexes, st, label='Soil Temperature')
    plt.xlabel('Readings (288/day)')
    plt.ylabel('Soil Temperature (°C)')
    plt.title('PT-1000')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('appdir/static/images/st.png')
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    return render_template('st.html', img_file=img_file)


@app.route("/lum")
@login_required
def lum():
    conn = db.engine.connect()
    df = pd.read_sql_table('sensor_data', conn)
    sorted = df.sort_values(by='rtctime', ascending=True)
    ttime = sorted['rtctime']
    lum = sorted['lum']
    x_indexes = np.arange(len(ttime))
    plt.figure(7)
    plt.style.use('fivethirtyeight')
    plt.bar(x_indexes, lum, label='Luminosity')
    plt.xlabel('Readings (288/day)')
    plt.ylabel('Illuminance (lux)')
    plt.title('Luminosity')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('appdir/static/images/lum.png')
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    return render_template('lum.html', img_file=img_file)


@app.route("/temp")
@login_required
def temp():
    conn = db.engine.connect()
    df = pd.read_sql_table('sensor_data', conn)
    sorted = df.sort_values(by='rtctime', ascending=True)
    ttime = sorted['rtctime']
    temp = sorted['temp']
    x_indexes = np.arange(len(ttime))
    plt.figure(8)
    plt.style.use('fivethirtyeight')
    plt.bar(x_indexes, temp, label='Temperature')
    plt.xlabel('Readings (288/day)')
    plt.ylabel('Celsius (°C)')
    plt.title('Temperature')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('appdir/static/images/temp.png')
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    return render_template('temp.html', img_file=img_file)


@app.route("/humd")
@login_required
def humd():
    conn = db.engine.connect()
    df = pd.read_sql_table('sensor_data', conn)
    sorted = df.sort_values(by='rtctime', ascending=True)
    ttime = sorted['rtctime']
    humd = sorted['humd']
    x_indexes = np.arange(len(ttime))
    plt.figure(9)
    plt.style.use('fivethirtyeight')
    plt.bar(x_indexes, humd, label='Humidity')
    plt.xlabel('Readings (288/day)')
    plt.ylabel('Percentage (%)')
    plt.title('humd')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('appdir/static/images/humd.png')
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    return render_template('humd.html', img_file=img_file)


@app.route("/pres")
@login_required
def pres():
    conn = db.engine.connect()
    df = pd.read_sql_table('sensor_data', conn)
    sorted = df.sort_values(by='rtctime', ascending=True)
    ttime = sorted['rtctime']
    pres = sorted['pres']
    pres = pres/101325
    x_indexes = np.arange(len(ttime))
    plt.figure(10)
    plt.style.use('fivethirtyeight')
    plt.bar(x_indexes, pres, label='Pressure')
    plt.xlabel('Readings (288/day)')
    plt.ylabel('Standard Atmosphere (atm)')
    plt.title('Pressure')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('appdir/static/images/pres.png')
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    return render_template('pres.html', img_file=img_file)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='no-reply@project.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit:
{url_for('reset_token', token=token, _external=True)}    
If you did not make this request, please ignore this email.
    '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect((url_for('account')))
    form = appdir.forms.RequestResetForm()
    if form.validate_on_submit():
        user = appdir.models.User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email sent with further instructions','info')
        return render_template(url_for('login'))
    return render_template('reset_request.html', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect((url_for('account')))
    user = appdir.models.User.verify_reset_token(token)
    if user is None:
        flash('Invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = appdir.forms.ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', form=form)