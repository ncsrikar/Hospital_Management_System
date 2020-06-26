import flask
from application import db

class Login_details(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(50))