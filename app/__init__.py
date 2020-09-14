from flask import Flask
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

from app.users import users
from app.main import main

app.register_blueprint(users)
app.register_blueprint(main)