from flask import render_template, url_for, flash, redirect, get_flashed_messages, request
from appdir import app, db, bcrypt
import appdir.models
# from appdir.models import User
import appdir.forms
# from appdir.forms import LoginForm, RegistrationForm
from flask_login import login_user, current_user, logout_user, login_required
import time


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


@app.route("/account")
@login_required
def account():
    sensor = appdir.models.Sensor.query.filter_by(owner=current_user.id).all()
    return render_template('account.html', title='Account', sensor=sensor)


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
    return render_template('data.html', NodeID=NodeID,pm1=pm1, pm2=pm2, pm3=pm3, am=am, vane_str=vane_str, sm=sm, temp=temp, humd=humd, pres=pres, lum=lum, bat=bat, timex=timex)