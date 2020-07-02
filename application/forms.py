from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,IntegerField,DateTimeField,SelectField
from wtforms.validators import DataRequired
# Contains the classes of all the forms used in the Website.Each form has an associated class, that can be found here. 
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    rememberme = BooleanField("rememberme")
    submit = SubmitField("Login")

class Register(FlaskForm): #Used for patient Registration
    patient_ssn_id = IntegerField("Patient SSN ID", validators=[DataRequired()])
    name = StringField("Name",validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    date = DateTimeField("Date",validators=[DataRequired()],format='%Y-%m-%dT%H:%M')
    type = SelectField("Type", choices=[('General ward','General ward'),('Semi Sharing','Semi Sharing'),('Single Room','Single Room')],validators=[DataRequired()])
    address = StringField("Address",validators=[DataRequired()])
    city = StringField("City",validators=[DataRequired()])
    state = StringField("State",validators=[DataRequired()])
    submit = SubmitField("Register")

class GetPatientInfo(FlaskForm): #Used to get the patient info from the user. 
    patient_id = IntegerField("Patient ID", validators=[DataRequired()])
    submit_get_details = SubmitField("Get Patient Details")

class UpdatePatientInfo(FlaskForm): #Used for updating the patient info. 
    patient_id_got = IntegerField("Patient ID", validators=[DataRequired()])
    patient_ssn_id = IntegerField("Patient SSN ID", validators=[DataRequired()])
    name = StringField("Name",validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    type = SelectField("Type", choices=[('General ward','General ward'),('Semi Sharing','Semi Sharing'),('Single Room','Single Room')])
    address = StringField("Address",validators=[DataRequired()])
    city = StringField("City",validators=[DataRequired()])
    state = StringField("State",validators=[DataRequired()])
    submit_update = SubmitField("Update Patient Details")

class GetMedicineNames(FlaskForm): #Used for verfying the quantiy of the selected medicine avaiable against the quantity entered. 
    medicine_name = SelectField("Medicine Name", choices = [])
    medicine_quantity = IntegerField("Quantity of Medicine to be Issued",validators=[DataRequired()])
    check_avialable = SubmitField("Check Availability")

class AddMedicine(FlaskForm): #Used for adding the medicine to the patient. Two fields here are similar to the above form to just store the values.
    name = StringField("Medicine Name")
    quantity = IntegerField("Quantity of Medicine to be Issued",validators=[DataRequired()])
    add = SubmitField("Add the Medicine")

class GetDiagnostics(FlaskForm): #Getting information of the Diagnostic
    test_name = SelectField("Test Name", choices= [])
    add_di = SubmitField("Get Info")

class AddDiagnostics(FlaskForm): #Adding the information to the patient the name field is written directly from the above form
    t_name = StringField("Test Name")
    t_add = SubmitField("Add Diagnostic")