from flask import render_template, url_for
from app.main import main

@main.route('/')
@main.route('/index')
def index():
    return render_template('home.html')