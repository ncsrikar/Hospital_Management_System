from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    rememberme = BooleanField("rememberme")
    submit = SubmitField("login")

class GetPatientInfo(FlaskForm):
    patient_id = IntegerField("Patient ID", validators=[DataRequired()])
    submit = SubmitField("get_patient")