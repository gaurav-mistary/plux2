import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'no-never-guess-142334-sfs343-35'
    