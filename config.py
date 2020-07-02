import os 
# Config object has all the details of the Database and the secret key to validate forms and for other security measures. 
class Config(object):
    SECRET_KEY = "b'A\xb4\t\xa3~\x16\xfb\xc3\x8f\xe1l\\V\x96\xfd\xaf'" #Generated using OS library of the python. 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql://admin:DpvvltHu32TgH96v9CvW@tcs.ciqjjxne9eri.us-east-1.rds.amazonaws.com:3306/tcs'
