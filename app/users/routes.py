from flask import render_template, url_for, redirect, flash, request
from app.users import users
from app.users.utils import send_verification_email
from app import db
from flask_login import login_user, current_user, logout_user, login_required
from app.users.forms import LoginForm, RegistrationForm, EmptyForm
from app.models import User
from werkzeug.urls import url_parse
from app.users.utils import generate_verification_code

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
        if not user.is_verified:
            next_url = url_for('users.verification_pending', username=user.username)
        else:
            next_url = request.args.get('next')
        
        if not next_url or url_parse(next_url).netloc != '':
            if not user.is_verified:
                next_url = url_for('users.verification_pending', username=user.username)
            else:
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
        send_verification_email(user)
        flash('Congratulations. You are now a registered user.', 'success')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', title='Register', form=form)

@users.route('/users/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out of session.', 'info')
    return redirect(url_for('main.index'))


@users.route('/users/<username>/verification_pending', methods=['GET', 'POST'])
@login_required
def verification_pending(username):
    user = User.query.filter_by(username=username).first()
    
    if user.is_verified:
        flash('User already verified', 'info')
        return redirect(url_for('main.index'))
    
    form = EmptyForm()
    if form.validate_on_submit():
        send_verification_email(user)
        flash('Verification Email sent. Please check your inbox', 'success')
        return redirect(url_for('users.verification_pending', username=user.username))
    
    return render_template('verification_pending.html',title='Verify User', user=user, form=form)


@users.route('/users/<username>/verify/<token>')
@login_required
def verify_user(username, token):
    user = User.verify_token(token)
    if user is None:
        flash('Sorry. Invalid Token', 'info')
        return redirect(url_for('users.verification_pending', username=username))
    
    user.is_verified = True
    db.session.commit()
    flash('User Verified', 'info')
    return redirect(url_for('main.index'))
