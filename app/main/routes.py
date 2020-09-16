from flask import render_template, url_for, redirect
from app.main import main
from flask_login import login_required, current_user

@main.route('/')
@main.route('/index')
def index():
    if current_user.is_authenticated:
        if not current_user.is_verified:
            return redirect(url_for('users.verification_pending', username=current_user.username))
    
    return render_template('home.html')