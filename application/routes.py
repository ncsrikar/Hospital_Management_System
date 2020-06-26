from application import app
from flask import render_template,request,redirect,flash,session
from application.forms import LoginForm,RegisterForm
from application.models import Login_details
courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]
#################################################################################################################





################################################################################################################
@app.route("/")
def index():
    return render_template("index.html", login= False, index=True,loggedin = session.get('email'))

@app.route("/courses")
@app.route("/courses/<term>")
def courses(term="Spring 2019"):
    

    return render_template("courses.html",courseData = courseData,courses=True,term=term)
@app.route("/login",methods=["GET","POST"])
def login():
    if(session.get('email')):
        return redirect("/")
    form = LoginForm()
   
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if(form.validate_on_submit()):
        cur.execute('SELECT * FROM logindata WHERE email = %s AND password = %s', (request.form.get("email"), request.form.get("password")))
        account = cur.fetchone()
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