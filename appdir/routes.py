from flask import render_template, url_for, flash, redirect, get_flashed_messages, request
from appdir import app, db, bcrypt
import appdir.models
# from appdir.models import User
import appdir.forms
# from appdir.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import os
import time
import secrets


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


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    img_file = url_for('static', filename='images/'+current_user.profile_pic)
    form = appdir.forms.PictureForm()
    if form.validate_on_submit():
        pic_file = save_pic(form.picture.data)
        current_user.profile_pic = pic_file
    sensor = appdir.models.Sensor.query.filter_by(owner=current_user.id).all()
    return render_template('account.html', title='Account', sensor=sensor, img_file=img_file, form=form)


@app.route("/data", methods=['GET', 'POST', 'PUT', 'DELETE'])
def data():
    NodeID = request.args.get('NodeID')
    pm1 = request.args.get('tpluviometer1')
    pm2 = request.args.get('tpluviometer2')
    pm3 = request.args.get('tpluviometer3')
    am = request.args.get('tanemometer')
    vane_str = request.args.get('twd')
    sm = request.args.get('tSoil_moist')
    temp = request.args.get('ttemp')
    humd = request.args.get('thumd')
    pres = request.args.get('tpres')
    lum = request.args.get('tLuminosity')
    bat = request.args.get('tbat')
    timex = request.args.get('ttime')
    form = appdir.forms.PictureForm()
    img_file = url_for('static', filename='images/' + current_user.profile_pic)
    return render_template('data.html', NodeID=NodeID,pm1=pm1, pm2=pm2, pm3=pm3, am=am, vane_str=vane_str, sm=sm, temp=temp, humd=humd, pres=pres, lum=lum, bat=bat, timex=timex, form=form, img_file=img_file)