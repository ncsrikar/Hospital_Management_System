import os 

class Config(object):
    SECRET_KEY = "b'A\xb4\t\xa3~\x16\xfb\xc3\x8f\xe1l\\V\x96\xfd\xaf'"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
