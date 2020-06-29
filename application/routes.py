from application import app,db
from flask import render_template,request,redirect,flash,session
from application.forms import LoginForm,Register, GetPatientInfo, UpdatePatientInfo
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
        accesslevel = user.accesslevel
        actual = request.form.get('password')
        if(check_password_hash(password,actual)):
            session['email'] = request.form.get("email")
            session['accesslevel'] = int(accesslevel)
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
    if(session.get("email")):
        if(session.get("accesslevel") == 1):
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
                patient_status = "Active"
                reg = Patient(patient_id = Patient_ID, patient_ssn = Patient_SSN_ID, patient_name = Patient_Name, patient_age = Patient_Age, patient_doj = Date_of_Admission, patient_rtype = Type_of_Bed, patient_address = Address, patient_state = State, patient_city = City,patient_status = patient_status)
            
                db.session.add(reg)
                db.session.commit()
                #return render_template("success.html")
                flash("Registeration Success", "success" )
            return render_template("register.html",patient=True,form=form)
        else:
            flash("Sorry! You don't have the required permission to view this page,contact administrator",'danger')
            return redirect("/")     
    else:
        flash("Sorry! You are not logged in Please LogIn",'danger')
        return redirect("/login")

@app.route("/patient")
def patient():
    if(session.get('email')):
        if(session.get("accesslevel") == 1):
            return render_template("patient.html", login= False, patient=True,loggedin = session.get('email'))
        else:
            flash("Sorry! You don't have the required permission to view this page,contact administrator",'danger')
            return redirect("/") 
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")

@app.route("/patient_update", methods=['GET', 'POST'])
def patientUpdate():
    if(session.get('email')):
        if(session.get("accesslevel") == 1):
            form = GetPatientInfo()
            form_details = UpdatePatientInfo()
            print(form.validate_on_submit(), form_details.is_submitted())
            if(form.validate_on_submit() or form_details.is_submitted()):
                print('Test')
                patient_id = request.form.get('patient_id')
                patient_details = Patient.query.filter_by(patient_id = patient_id).first()
                if(patient_details is None):
                    flash('No Patient Found', 'danger')
                if(request.form.get('patient_id_got')):
                    patient_id_got = request.form.get('patient_id_got')
                    patient_details_update = Patient.query.filter_by(patient_id = patient_id_got).first()
                    patient_details_update.patient_ssn = request.form.get('patient_ssn_id')
                    patient_details_update.patient_name = request.form.get('name')
                    patient_details_update.patient_age = request.form.get('age')
                    patient_details_update.patient_rtype = request.form.get('type')
                    patient_details_update.patient_address = request.form.get('address')
                    patient_details_update.patient_city = request.form.get('city')
                    patient_details_update.patient_state = request.form.get('state')
                    print(patient_details_update.patient_city)
                    db.session.commit()
                    flash('Patient Details Updated Successfully', 'success')
                    return render_template("patient_update.html", login= False, patient=True,loggedin = session.get('email'), form=form)
                return render_template("patient_update.html", login= False, patient=True,loggedin = session.get('email'), form=form, form_details = form_details, patient_details = patient_details)
            else:
                return render_template("patient_update.html", login= False, patient=True,loggedin = session.get('email'), form=form)
        else:
            flash("Sorry! You don't have the required permission to view this page,contact administrator",'danger')
            return redirect("/")  
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")

@app.route("/patient_view", methods=['GET', 'POST'])
def patientView():
    if(session.get('email')):
        if(session.get("accesslevel") == 1):
            form = GetPatientInfo()
            if(form.validate_on_submit()):
                print('Test')
                patient_id = request.form.get('patient_id')
                patient_details = Patient.query.filter_by(patient_id = patient_id).first()
                if(patient_details is None):
                    flash('No Patient Found', 'danger')
                return render_template("patient_view.html", login= False, patient=True,loggedin = session.get('email'), form=form, patient_details = patient_details)
            else:
                return render_template("patient_view.html", login= False, patient=True,loggedin = session.get('email'), form=form)
        else:
            flash("Sorry! You don't have the required permission to view this page,contact administrator",'danger')
            return redirect("/")  
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")

@app.route("/view_all", methods=['GET'])
def viewAll():
    if(session.get('email')):
        if(session.get("accesslevel") == 1):
            view_det = Patient.query.order_by(Patient.patient_id).all()
            if(view_det is None):
                flash('No Patient Found', 'danger')
            # return render_template("patient_view.html", login= False, patient=True,loggedin = session.get('email'), form=form, view_det = view_det)
            else:
                return render_template("view_all.html", login= False, patient=True,loggedin = session.get('email'))
        else:
            flash("Sorry! You don't have the required permission to view this page,contact administrator",'danger')
            return redirect("/")
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")


@app.route("/patient_delete", methods=['GET', 'POST'])
def patientDelete():
    if(session.get('email')):
        if(session.get("accesslevel") == 1):
            form = GetPatientInfo()
            if(form.validate_on_submit()):
                print('Test')
                patient_id = request.form.get('patient_id')
                patient_details = Patient.query.filter_by(patient_id = patient_id).first()
                if(patient_details is None):
                    flash('No Patient Found', 'danger')
                return render_template("patient_delete.html", login= False, patient=True,loggedin = session.get('email'), form=form, patient_details = patient_details)
            else:
                return render_template("patient_delete.html", login= False, patient=True,loggedin = session.get('email'), form=form)
        else:
            flash("Sorry! You don't have the required permission to view this page,contact administrator",'danger')
            return redirect("/")
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")

@app.route('/patient_delete_confirm')
def deletePatient():
    if(session.get('email')):
        if(session.get("accesslevel") == 1):
            patient_id = request.args.get('id')
            print(patient_id)
            patient_details = Patient.query.filter_by(patient_id = patient_id).first()
            db.session.delete(patient_details)
            db.session.commit()
            flash('Patient Delete Successful', 'success')
            return redirect('/patient')
        else:
            flash("Sorry! You don't have the required permission to perform this operation, contact administrator",'danger')
            return redirect("/")
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")

@app.route("/medicines")
def medicines():
    if(session.get('email')):
        if(session.get("accesslevel")==1 or session.get("accesslevel")==2):
            return render_template("index.html", login= False, medicines=True,loggedin = session.get('email'))
        else:
            flash("Sorry! You don't have the required permission to view this page,contact administrator",'danger')
            return redirect("/")
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")
@app.route("/diagnostics")
def diagnostics():
    if(session.get('email')):
        if(session.get("accesslevel")==1 or session.get("accesslevel")==3):
            return render_template("index.html", login= False, diagnostics=True,loggedin = session.get('email'))
        else:
            flash("Sorry! You don't have the required permission to view this page,contact administrator",'danger')
            return redirect("/")
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")