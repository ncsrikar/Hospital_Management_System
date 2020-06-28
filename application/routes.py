from application import app,db
from flask import render_template,request,redirect,flash,session
from application.forms import LoginForm,Register
from application.models import login_details,Patient
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
@app.route("/")
def index():
    return render_template("index.html", login= False, index=True,loggedin = session.get('email'))

@app.route("/login",methods=["GET","POST"])
def login():
    if(session.get('email')):
        return redirect("/")
    
    form = LoginForm()

    if(form.validate_on_submit()):

        user= login_details.query.filter_by(email=request.form.get('email')).first()
        password = user.password
        actual = request.form.get('password')
        if(check_password_hash(password,actual)):
            session['email'] = request.form.get("email")
            return redirect("/") 
        else:
            flash("Oops! Something is wrong","danger")
    return render_template("login.html",login=True,form = form)
@app.route("/logout")
def logout():
    session['email'] = False
    return redirect("/")


@app.route("/register", methods = ['GET', 'POST'])
def register():
    form = Register()
    if request.method == "POST":
        Patient_SSN_ID = request.form['patient_ssn_id']
        Patient_Name = request.form['name']
        Patient_Age = request.form['age']
        Date_of_Admission = datetime.strptime(request.form.get("date"), '%Y-%m-%dT%H:%M')
        Date_of_Admission.strftime("%Y-%m-%d %H:%M:%S")
    
        Type_of_Bed = request.form['type']
        Address = request.form['address']
        State  =request.form['state']
        City = request.form['city']
        count = len(Patient.query.all()) + 1
        print(Patient.query.column_descriptions)
        Patient_ID = int('0'*(9-count) + str(count))
        patient_status = "Something"
        reg = Patient(patient_id = Patient_ID, patient_ssn = Patient_SSN_ID, patient_name = Patient_Name, patient_age = Patient_Age, patient_doj = Date_of_Admission, patient_rtype = Type_of_Bed, patient_address = Address, patient_state = State, patient_city = City,patient_status = patient_status)
     
        db.session.add(reg)
        db.session.commit()
        #return render_template("success.html")
        flash("Registeration Success", "success" )
    return render_template("register.html",register=True,form=form)

@app.route("/patient")
def patient():
    if(session.get('email')):
        return render_template("index.html", login= False, patient=True,loggedin = session.get('email'))
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")

@app.route("/medicines")
def medicines():
    if(session.get('email')):
        return render_template("index.html", login= False, medicines=True,loggedin = session.get('email'))
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")
@app.route("/diagnostics")
def diagnostics():
    if(session.get('email')):
        return render_template("index.html", login= False, diagnostics=True,loggedin = session.get('email'))
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")