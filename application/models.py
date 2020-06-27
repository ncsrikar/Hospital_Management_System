import flask
from application import db
print(db)
class Login_details(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(300))
    accesslevel = db.Column(db.Integer)
    