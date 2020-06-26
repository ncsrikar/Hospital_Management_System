import os 

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or "b'A\xb4\t\xa3~\x16\xfb\xc3\x8f\xe1l\\V\x96\xfd\xaf'"

