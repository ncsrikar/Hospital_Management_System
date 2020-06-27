import flask
from application import db
print(db)
class login_details(db.Model):
    __tablename__ = 'login_details'
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))
    accesslevel = db.Column(db.Integer)
    