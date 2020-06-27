from application import app,db
from flask import render_template,request,redirect,flash,session
from application.forms import LoginForm
from application.models import Login_details


@app.route("/")
def index():
    return render_template("index.html", login= False, index=True,loggedin = session.get('email'))

@app.route("/login",methods=["GET","POST"])
def login():
    if(session.get('email')):
        return redirect("/")
    
    form = LoginForm()
    account = ""

    if(form.validate_on_submit()):
        user = Login_details.query.filter
        account = True
        if(account):
            session['email'] = request.form.get("email")
            return redirect("/") 
        else:
            flash("Oops! Something is wrong","danger")
    return render_template("login.html",login=True,form = form)
@app.route("/logout")
def logout():
    session['email'] = False
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html",register=True)

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