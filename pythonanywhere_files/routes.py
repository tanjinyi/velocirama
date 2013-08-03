import sqlite3
from datetime import datetime
from flask import *
from flask_mail import *
from functools import wraps
from flask.ext.wtf import *
from wtforms import *
from werkzeug import generate_password_hash, check_password_hash

MERCHANDISE = "merchandise.db"
DATABASE = "data.db"

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'secret key is secret,'

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Please login to see these pages')
            return redirect(url_for('log'))
    return wrap

@app.route('/clear/', methods=['POST', 'GET'])
def clear():
    if request.method == 'POST':
        password=request.form['password']
        if hash(password)==8810862850339964589:
            with sqlite3.connect("everything.db") as connection:
                c = connection.cursor()
                c.execute("DROP TABLE IF EXISTS ads")
                c.execute("CREATE TABLE ads((aid INT, qrcode TEXT, filename TEXT, startdate DATE, enddate DATE, starttime TIME, endtime TIME))")
            return 'Dear administrator: clear up alr:)'
        else:
            return 'Please do not hack my site :)'
    else:
        return render_template('clear.html')

def save_ad(aid, qrcode, filename, startdate, enddate, starttime, endtime):
    with sqlite3.connect("everything.db") as connection:
        c = connection.cursor()
        c.execute("SELECT ad_id FROM ads")
        total = c.fetchall()
    max_id = 1
    for s in total:
        if s[0] > max_id:
            max_id = s[0]
    if len(total)>0:
        max_id = max_id + 1
    with sqlite3.connect("everything.db") as connection:
        c = connection.cursor()
        c.execute("INSERT INTO ads VALUES(?,?,?,?,?,?,?)" , (aid, qrcode, filename, startdate, enddate, starttime, endtime))
    return True

class login_form(Form):
    username = TextField('Username:', [validators.Required()])
    password = PasswordField('Password:', [validators.Required()])
    submit = SubmitField("Submit")

@app.before_request
def load_user():
    if 'user' in session:
        user = session["user"]
    else:
        user = "Guest"
    g.user = user
    
@app.route('/')
def index():
    return render_template('index.html', user=g.user)
    
@app.route("/log", methods=["GET", "POST"])
def log():
    form = login_form()
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        if user == "":
            flash("Oops! Username was not entered")
        elif pw == "":
            flash("Oops! Password was not entered")
        else:
            if user == "admin" and pw == "admin":
                session['user'] = user
                session['logged_in'] = True
                message = "You have successfully logged in"
                return render_template('index.html', message=message)
            elif user =="admin" and pw != "admin":
                flash("Oops! Wrong password") 
            elif user!="admin" and pw == "admin":
                flash("Oops! Wrong username")
            else:
                flash("Oops! This is not a valid user")
        return render_template("log.html", form=form)
    return render_template("log.html", form=form)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/create')
@login_required
def create():
    if request.method == 'POST':
        qrcode = request.form['qrcode']
        f = request.files['image']
        filename = f.filename
        description = request.form['description']
        save_ad(aid, qrcode, filename, startdate, enddate, starttime, endtime)
    return render_template('create.html')

@app.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')

@app.route('/source')
@login_required
def source():
    return render_template('source.html')

                                   
if __name__ == '__main__':
    app.run(debug=True)
