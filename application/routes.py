from application import app,db
from flask import render_template,request,redirect,flash,session
from application.forms import LoginForm,Register, GetPatientInfo, UpdatePatientInfo,GetMedicineNames,AddMedicine, GetDiagnostics, AddDiagnostics
from application.models import login_details,Patient,Patient_Medicine,Medicine, Tests, Patient_Tests
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
################
@app.route("/")
def index():
    return render_template("index.html", login= False, index=True,loggedin = session.get('email'))
##############################
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
#########################
@app.route("/logout")
def logout():
    session['email'] = False
    session['accesslevel'] =False
    return redirect("/")

##############################
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
###########################################################
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
##################################################################
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
#####################################################

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
####################################################

@app.route("/view_all", methods=['GET'])
def viewAll():
    if(session.get('email')):
        if(session.get("accesslevel") == 1):
            view_det = Patient.query.order_by(Patient.patient_id).all()
            if(view_det is None):
                flash('No Patient Found', 'danger')
                return render_template("view_all.html", login= False, patient=True,loggedin = session.get('email'), view_det = view_det)
            else:
                return render_template("view_all.html", login= False, patient=True,loggedin = session.get('email'), view_det = view_det)
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
######################################################

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
########################################################
names_medicines = []
@app.route("/medicines" , methods=['GET', 'POST'])
def medicines():
    global names_medicines
    names_medicines = []
    if(session.get('email')):
        if(session.get("accesslevel")==1 or session.get("accesslevel")==2):
            form = GetPatientInfo()
            if(form.validate_on_submit()):
                print('Test')
                patient_id = request.form.get('patient_id')
                patient_details = Patient.query.filter_by(patient_id = patient_id).first()
                if(patient_details is None):
                    flash('No Patient Found', 'danger')
                else:
                    medicines = Patient_Medicine.query.filter_by(patient_id = patient_id).all()
                    
                    for i in medicines:
                        quant_issued = i.quantity_issued
                        medicine = Medicine.query.filter_by(medicine_id = i.medicine_id).first()
                        name = medicine.medicine_name
                        rate = medicine.medicine_rate
                        price = quant_issued*rate
                        names_medicines.append((name,quant_issued,rate,price))
                    print(names_medicines)
                return render_template("medicines.html", login= False, medicines=True,loggedin = session.get('email'), form=form, patient_details = patient_details,names_medicines = names_medicines)
            else:
                return render_template("medicines.html", login= False, medicines=True,loggedin = session.get('email'), form=form)
            return render_template("medicines.html", login= False, medicines=True,loggedin = session.get('email'))
        else:
            flash("Sorry! You don't have the required permission to view this page,contact administrator",'danger')
            return redirect("/")
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")
############################################################

@app.route("/issue_medicines/<patient_id>/<medicine_id>",methods=['GET', 'POST'])
def issue_medicines(patient_id,medicine_id):
    if(session.get('email')):
        if(session.get("accesslevel")==1 or session.get("accesslevel")==2):
            form = GetMedicineNames()
            form_add = AddMedicine()
            medicines = Medicine.query.order_by(Medicine.medicine_id).all()
            form.medicine_name.choices = [(medicine.medicine_name,medicine.medicine_name) for medicine in medicines]
            form.medicine_name.choices = [(0, "Choose a Medicine")] +form.medicine_name.choices

            if(form.validate_on_submit() or form_add.is_submitted()):
                name = request.form.get("medicine_name") 
                quantity = request.form.get("medicine_quantity")
                
  
                if(name == None):
                    name = request.form.get("name")
                if(quantity == None):
                    quantity = request.form.get("quantity")
                quantity = int(quantity)
                id = Medicine.query.filter_by(medicine_name = name).first().medicine_id
                rate = Medicine.query.filter_by(medicine_name = name).first().medicine_rate
                total_cost = quantity*rate
                if(name == '0'):
                    flash("Please select a valid Option","danger")
                    return render_template("issue_medicine.html",medicine = True, availabilty = 0, form = form,loggedin = session.get('email'))
                    
                quant = Medicine.query.filter_by(medicine_name = name).first().medicine_quantity 
                if(quantity<quant):
                    availabilty = True
                    print("here")
                    if(request.form.get("quantity")):
                        print("Just here")
                        quantity = request.form.get("quantity")
                        quantity = int(quantity)
                        patient_id = int(patient_id)
                        all_medicines = Patient_Medicine.query.filter_by(patient_id = patient_id).all()
                        all_medicineslist = []
                        for i in all_medicines:
                            all_medicineslist.append(i.medicine_id)
                        if(id in all_medicineslist):
                            patient_medicine = Patient_Medicine.query.filter_by(medicine_id = id,patient_id = int(patient_id)).first()
                            patient_medicine.quantity_issued = patient_medicine.quantity_issued+ quantity
                            db.session.commit()
                            flash("Updated the Value of the existing medicine and updated stock","success")
                        else:
                            new_medicine = Patient_Medicine(patient_id = patient_id, medicine_id = id, quantity_issued = quantity)
                            db.session.add(new_medicine)
                            db.session.commit()
                            flash("Successfully added new medicine to the patient and updated stock","success")
                        change_total_medicines = Medicine.query.filter_by(medicine_id = id).first()
                        change_total_medicines.medicine_quantity = change_total_medicines.medicine_quantity-quantity
                        db.session.commit()
                        return render_template("issue_medicine.html", medicine=True, availabilty = 0, form = form,loggedin = session.get('email'),name = name,quantity = quantity,rate= rate, total_cost = total_cost)
                        # else:
                            
                        #     return render_template("issue_medicine.html", availabilty = availabilty, form = form,form_add = form_add,loggedin = session.get('email'),name = name)
                    return render_template("issue_medicine.html", medicine=True, availabilty = availabilty, form = form,form_add = form_add,loggedin = session.get('email'),name = name,quantity = quantity,rate= rate, total_cost = total_cost)
                else:
                    availabilty = False
                    flash("Please select value less than {}".format(quant),"danger")
                    return render_template("issue_medicine.html", medicine=True, availabilty = availabilty, form = form,loggedin = session.get('email'))
                
                
            else:
                print("here I am ")
                return render_template("issue_medicine.html", medicine=True, form = form,loggedin = session.get('email'))  
        else:
            flash("Sorry! You don't have the required permission to view this page,contact administrator",'danger')
            return redirect("/index")
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")


##############################################################
names_diag = []
@app.route("/diagnostics", methods = ['GET', 'POST'] )
def diagnostics():
    global names_diag
    names_diag = []
    if(session.get('email')):
        if(session.get("accesslevel")==1 or session.get("accesslevel")==3):
            form = GetPatientInfo()
            if(form.validate_on_submit()):
                print('Test')
                patient_id = request.form.get('patient_id')
                patient_details = Patient.query.filter_by(patient_id = patient_id).first()
                if(patient_details is None):
                    flash('No Patient Found', 'danger')
                else:
                    diagnostics = Patient_Tests.query.filter_by(patient_id = patient_id).all()
                    
                    for i in diagnostics:
                        # quant_issued = i.quantity_issued
                        test = Tests.query.filter_by(test_id = i.test_id).first()
                        name = test.test_name
                        charge = test.test_charge
                        # price = quant_issued*rate
                        names_diag.append((name,charge))
                    print(names_diag)
                return render_template("diagnostics.html", login= False, diagnostics=True,loggedin = session.get('email'), form=form, patient_details = patient_details,names_diag = names_diag)
            else:
                return render_template("diagnostics.html", login= False, diagnostics=True,loggedin = session.get('email'), form=form)
            return render_template("diagnostics.html", login= False, diagnostics=True,loggedin = session.get('email'))
        else:
            flash("Sorry! You don't have the required permission to view this page,contact administrator",'danger')
            return redirect("/")
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")
#############################################################

@app.route("/add_diagnostics/<patient_id>/<test_id>",methods=['GET', 'POST'])
def add_diagnostics(test_id, patient_id):
    if(session.get('email')):
        if(session.get("accesslevel")==1 or session.get("accesslevel")==3):
            form = GetDiagnostics()
            form_add = AddDiagnostics()
            diagnostics = Tests.query.order_by(Tests.test_id).all()
            form.test_name.choices = [(diag.test_name, diag.test_name) for diag in diagnostics]
            form.test_name.choices = [(0, "Choose a Test")] +form.test_name.choices

            if(form.validate_on_submit() or form_add.is_submitted()):
                name = request.form.get("test_name") 
                
  
                if(name == None):
                    name = request.form.get("t_name")
                id = Tests.query.filter_by(test_name = name).first().test_id
                charge = Tests.query.filter_by(test_name = name).first().test_charge
                
                if(name == '0'):
                    flash("Please select a valid Option","danger")
                    return render_template("add_diag.html", form = form,loggedin = session.get('email'))
                     
                if(request.form.get("t_name")):
                    patient_id = int(patient_id)
                    all_tests = Patient_Tests.query.filter_by(patient_id = patient_id).all()
                    all_testlist = []
                    for i in all_tests:
                        all_testlist.append(i.test_id)
                        if(id in all_testlist):
                            patient_test = Patient_Tests.query.filter_by(test_id = id,patient_id = int(patient_id)).first()
                            db.session.commit()
                            # flash("","success")
                        else:
                            new_test = Patient_Tests(test_id = id, patient_id = patient_id)
                            db.session.add(new_test)
                            db.session.commit()
                            flash("Successfully added new diagnostic test","success")
                            
                    db.session.commit()
                    return render_template("add_diag.html",diagnostics=True, form = form, form_add = form_add, loggedin = session.get('email'),name = name,charge= charge)

                else:
                    return render_template("add_diag.html",diagnostics=True, form = form, form_add = form_add, loggedin = session.get('email'),name = name,charge= charge)


                
            else:
                print("here I am ")
                return render_template("add_diag.html",diagnostics=True, form = form,loggedin = session.get('email'))  
        else:
            flash("Sorry! You don't have the required permission to view this page,contact administrator",'danger')
            return redirect("/index")
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")

@app.route("/patient_discharge")
def patientDischarge():
    names_medicines = []
    names_diag = []
    medicine_total = 0
    diag_total = 0
    ward_charges = 0
    general_price = 2000
    semi_price = 4000
    single_price = 8000
    room_price = 0
    if(session.get('email')):
        if(session.get("accesslevel") == 1):
            patient_id = request.args.get('id')
            print(patient_id)
            patient_details = Patient.query.filter_by(patient_id = patient_id).first()
            if(patient_details is None):
                flash('No Patient Found', 'danger')
            else:
                today = datetime.today()
                days = (today - patient_details.patient_doj).days
                print(int(days))
                if(patient_details.patient_rtype == 'General ward'):
                    ward_charges = general_price * int(days)
                    room_price = general_price
                elif(patient_details.patient_rtype == 'Semi Sharing'):
                    ward_charges = semi_price * int(days)
                    room_price = semi_price
                elif(patient_details.patient_rtype == 'Single Room'):
                    ward_charges = single_price * int(days)
                    room_price = single_price

                print(ward_charges)
                medicines = Patient_Medicine.query.filter_by(patient_id = patient_id).all()
                
                for i in medicines:
                    quant_issued = i.quantity_issued
                    medicine = Medicine.query.filter_by(medicine_id = i.medicine_id).first()
                    name = medicine.medicine_name
                    rate = medicine.medicine_rate
                    price = quant_issued*rate
                    medicine_total = medicine_total + price
                    names_medicines.append((name,quant_issued,rate,price))
                print(names_medicines)
                diagnostics = Patient_Tests.query.filter_by(patient_id = patient_id).all()
                    
                for i in diagnostics:
                    test = Tests.query.filter_by(test_id = i.test_id).first()
                    name = test.test_name
                    charge = test.test_charge
                    diag_total = diag_total + charge
                    names_diag.append((name,charge))
                print(names_diag)
            return render_template("billing.html", patient = True, loggedin = session.get('email'), patient_details = patient_details,names_medicines = names_medicines, medicine_total = medicine_total, ward_charges = ward_charges, days = days, room_price = room_price, names_diag = names_diag, diag_total = diag_total)
        else:
            flash("Sorry! You don't have the required permission to perform this operation, contact administrator",'danger')
            return redirect("/")
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")

@app.route('/confirm_discharge')
def discharge():
    if(session.get('email')):
        if(session.get("accesslevel") == 1):
            patient_id = request.args.get('id')
            print(patient_id)
            patient_details = Patient.query.filter_by(patient_id = patient_id).first()
            if(patient_details is None):
                flash('No Patient Found', 'danger')
            else:
                patient_details.patient_status = 'Discharged'
                db.session.commit()
                flash('Patient Discharge Successful', 'success')

            return redirect("/patient")
        else:
            flash("Sorry! You don't have the required permission to perform this operation, contact administrator",'danger')
            return redirect("/")
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")