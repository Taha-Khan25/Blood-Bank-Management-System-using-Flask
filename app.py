from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
from flask.helpers import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, login_user, login_manager, LoginManager
from flask_login import UserMixin

app = Flask(__name__)
app.secret_key = "bloodbankproject"


# this is for getting the unique user access
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3307/bloodbank'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3307",
    passwd="",
    database="bloodbank"
)

my_cursor = mydb.cursor()
my_cursor1 = mydb.cursor()


class User(UserMixin, db.Model):
    username = db.Column(db.String(15), primary_key=True)
    email = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(1000), nullable=False)
    donorname = db.Column(db.String(30), nullable=False)
    phoneno = db.Column(db.String(10), nullable=False)
    bloodgroup = db.Column(db.String(5), nullable=False)


class Donor(db.Model):
    donor_id = db.Column(db.Integer, primary_key=True)
    donorname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    weight = db.Column(db.String(10), nullable=False)
    age = db.Column(db.String(10), nullable=False)
    phoneno = db.Column(db.String(10), nullable=False)
    bloodgroup = db.Column(db.String(5), nullable=False)


class Bloodreq(db.Model):
    paitent_id = db.Column(db.Integer, primary_key=True)
    paitentname = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    age = db.Column(db.String(10), nullable=False)
    phoneno = db.Column(db.String(10), nullable=False)
    bloodgroup = db.Column(db.String(5), nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    bloodtype = db.Column(db.String(10), nullable=False)\



class Blood(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    bloodgroup = db.Column(db.String(5), nullable=False)
    unit = db.Column(db.String(10), nullable=False)


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get((user_id))


@app.route("/test")
def test():
    try:
        a = Test.query.all()
        print(a)
        return f'MY DATABASE IS CONNECTED'
    except Exception as e:
        print(e)
        return f'MY DATABASE IS NOT CONNECTED {e}'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username= request.form['username']
        email = request.form['email']
        dob = request.form['dob']
        name = request.form['donorname']
        phoneno = request.form['phoneno']
        bloodgroup = request.form['bloodgroup']
        encpassword = generate_password_hash(dob)

        user = User.query.filter_by(email=email).first()
        username1 = User.query.filter_by(username=username).first()

        if user:
            flash("Email is already taken", "warning")
            return render_template("signup.html")
        if username1:
            flash("Username is already taken", "warning")
            return render_template("signup.html")

        my_cursor.execute("INSERT INTO User(username, email, dob, donorname, phoneno, bloodgroup)  VALUES (%s,%s,%s,%s,%s,%s)",
                          (username, email, encpassword, name, phoneno, bloodgroup))
        mydb.commit()
        mydb.close()
        flash("SignUp Success Please Login", "success")
    return render_template('signup.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        dob = request.form.get('dob')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.dob, dob):
            flash("Please check your login details and try again.", "danger")
            return render_template("login.html")
        else:
            return render_template("index.html")
    return render_template("login.html")

@app.route('/adminlogin', methods=['POST', 'GET'])
def adminlogin():
    if request.method == 'POST':
        email = request.form.get('email')
        dob = request.form.get('dob')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.dob, dob):
            flash("Please check your login details and try again.", "danger")
            return render_template("adminlogin.html")
        else:
            return render_template("index.html")
    return render_template("adminlogin.html")


@app.route('/bloodreqst', methods=['POST', 'GET'])
def bloodreqst():
    if request.method == 'POST':
        paitentname = request.form['paitentname']
        dob = request.form['dob']
        age = request.form['age']
        phoneno = request.form['phoneno']
        bloodgroup = request.form['bloodgroup']
        unit = request.form['unit']
        bloodtype = request.form['bloodtype']

        my_cursor.execute("INSERT INTO Bloodreq(paitentname, dob, age, phoneno, bloodgroup ,unit,bloodtype)  VALUES (%s,%s,%s,%s,%s,%s,%s)",
                          (paitentname, dob, age, phoneno, bloodgroup, unit, bloodtype))
        mydb.commit()
        flash("Request Added Succesfully", "success")
    return render_template("requests.html")


@app.route('/donors', methods=['POST', 'GET'])
def donors():
    if request.method == 'POST':
        donorname = request.form['donorname']
        email = request.form['email']
        dob = request.form['dob']
        weight = request.form['weight']
        age = request.form['age']
        phoneno = request.form['phoneno']
        bloodgroup = request.form['bloodgroup']

        my_cursor.execute("INSERT INTO Donor(donorname, email, dob, weight, age, phoneno, bloodgroup)  VALUES (%s,%s,%s,%s,%s,%s,%s)",
                          (donorname, email, dob, weight, age, phoneno, bloodgroup))
        mydb.commit()
        # mydb.close()
        flash("Donor Added Succesfully", "success")
    return render_template("donor.html")


@app.route('/donorlist')
def donorlist():
    data = Donor.query.all()
    return render_template('donorlist.html', data=data)


@app.route('/bloodbank')
def bloodbank():
    data = Blood.query.all()
    return render_template('bloodbank.html', data=data)


@app.route('/reqlist')
def reqlist():
    data = Bloodreq.query.all()
    return render_template('reqlist.html', data=data)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul", "succes")
    return redirect(url_for('login'))


@app.route('/update/<int:paitent_id>', methods=['GET', 'POST'])
def update(paitent_id):
    if request.method == 'POST':
        paitentname = request.form['paitentname']
        dob = request.form['dob']
        age = request.form['age']
        phoneno = request.form['phoneno']
        bloodgroup = request.form['bloodgroup']
        unit = request.form['unit']
        bloodtype = request.form['bloodtype']
        todo = Bloodreq.query.filter_by(paitent_id=paitent_id).first()
        todo.paitentname = paitentname
        todo.dob = dob
        todo.age = age
        todo.phoneno = phoneno
        todo.bloodgroup = bloodgroup
        todo.unit = unit
        todo.bloodtype = bloodtype

        db.session.add(todo)
        db.session.commit()
        flash("Update Succesfull", "success")
        return redirect("/reqlist")

    todo = Bloodreq.query.filter_by(paitent_id=paitent_id).first()
    return render_template('update.html', todo=todo)


@app.route('/updatebank/<int:sno>', methods=['GET', 'POST'])
def updatebank(sno):
    if request.method == 'POST':
        unit = request.form['unit']
        todo = Blood.query.filter_by(sno=sno).first()
        todo.unit = unit
        db.session.add(todo)
        db.session.commit()
        return redirect("/bloodbank")

    todo = Blood.query.filter_by(sno=sno).first()
    return render_template('bankupdate.html', todo=todo)


@app.route('/deletereq/<int:paitent_id>')
def deletereq(paitent_id):
    todo = Bloodreq.query.filter_by(paitent_id=paitent_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('reqlist'))


@app.route('/deletedonor/<int:donor_id>')
def deletedonor(donor_id):
    todo = Donor.query.filter_by(donor_id=donor_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('donorlist'))


if __name__ == '__main__':
    app.run(debug=True)
