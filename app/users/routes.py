from flask import render_template, url_for, redirect, flash, request
from app.users import users
from app import db
from flask_login import login_user, current_user, logout_user, login_required
from app.users.forms import LoginForm, RegistrationForm
from app.models import User
from werkzeug.urls import url_parse

@users.route('/users/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.verify_password(form.password.data):
            flash('Invalid Credentials. Please re-enter', 'danger')
            return redirect(url_for('users.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_url = request.args.get('next')
        if not next_url or url_parse(next_url).netloc != '':
            next_url = url_for('main.index')
        flash('Login Successfull', 'success')
        return redirect(next_url)
    
    return render_template('login.html', title='Login', form=form)

@users.route('/users/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            fname = form.fname.data,
            lname = form.lname.data,
            username = form.username.data,
            email = form.email.data,
            about_me = form.about_me.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations. You are now a registered user.', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', title='Register', form=form)

@users.route('/users/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out of session.', 'info')
    return redirect(url_for('main.index'))
