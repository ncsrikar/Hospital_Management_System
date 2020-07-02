import flask
from application import db
from datetime import datetime

#Each table has a class created here. It is the model of the table and is used to interact with it. 
class login_details(db.Model):
    __tablename__ = 'login_details' #Contains the email and hashed password of the 3 users. 
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True)
    password = db.Column(db.String(255))
    accesslevel = db.Column(db.Integer)

class Patient(db.Model):
    __tablename__ = 'patient_details' # Contains all the details of the patient. 
    patient_id = db.Column(db.Integer, primary_key = True)
    patient_ssn = db.Column(db.Integer)
    patient_name = db.Column(db.String(255))
    patient_address= db.Column(db.String(1000))
    patient_city =  db.Column(db.String(255))
    patient_state =  db.Column(db.String(255))
    patient_age = db.Column(db.Integer)
    patient_doj = db.Column(db.DateTime, default = datetime.now)
    patient_rtype = db.Column(db.String(255))
    patient_status = db.Column(db.String(255))

class Medicine(db.Model):
    __tablename__ ="medicines"  # contains all the available medicines in the hospital and their available quantities. 
    medicine_id = db.Column(db.Integer, primary_key = True)
    medicine_name = db.Column(db.String(255))
    medicine_rate = db.Column(db.Integer)
    medicine_quantity = db.Column(db.Integer)


class Patient_Medicine(db.Model):
    __tablename__ ="patient_medicine" # Contains Patient ID against the IDs of the medicines issued to them. 
    id = db.Column(db.Integer,primary_key = True)
    patient_id = db.Column(db.Integer)
    medicine_id = db.Column(db.Integer)
    quantity_issued = db.Column(db.Integer)

class Tests(db.Model):
    __tablename__ = "tests" # Contains all the test available in the hospital. 
    test_id = db.Column(db.Integer, primary_key = True)
    test_name = db.Column(db.String(255))
    test_charge = db.Column(db.Integer)

class Patient_Tests(db.Model):
    __tablename__ = "patient_tests" #Contains Patient ID against the IDs of the tests assinged to them. 
    id = db.Column(db.Integer,primary_key = True)
    test_id = db.Column(db.Integer)
    patient_id = db.Column(db.Integer)
    