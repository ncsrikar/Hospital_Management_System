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
        if(account):
            flash("Logged in Successfully","success")
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
@app.route("/enrollment",methods = ["GET","POST"])
def enrollment():
    if(session.get('email')):
        id = request.form.get("courseID")
        title = request.form.get("title")
        term = request.form.get("term")
        print(id,title,term)
        if(id):
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM `customer`.`enrollment` WHERE email = %s AND courseid = %s', (session.get('email'),id))
            account = cur.fetchone()
            if(account):
                flash("Looks like you have already registered","danger")
                return redirect("/courses")
            else:
                cur.execute("INSERT INTO `customer`.`enrollment` (`Sno`,`email`, `courseid`, `coursetitle`, `term`) VALUES (%s, %s, %s, %s)",(0,session.get('email'),id, title,term))
                mysql.connection.commit() 
            return render_template("enrollment.html",enrollment=True,id=id,title=title,term=term,selectedcourses = None)
        else:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM `customer`.`enrollment`')
            alldata = cur.fetchall()
            print(alldata)
            return render_template("enrollment.html",enrollment=True,id=id,title=title,term=term,selectedcourses = alldata)
    else:
        flash("looks like you are not logged in! Please log in","danger")
        return redirect("/login")