from flask import Flask, request, render_template,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user,logout_user,UserMixin
import pymysql as sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']= 'abcd1123@'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

sql.install_as_MySQLdb()
class Users(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    phoneno = db.Column(db.String(120))
    email = db.Column(db.String(80))
    password = db.Column(db.String(120))
    repassword = db.Column(db.String(80))
    address = db.Column(db.String(120))

class Addcontact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    phoneno = db.Column(db.String(120))
    subject = db.Column(db.String(120))
    address = db.Column(db.String(80))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(id)

@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()
        if user and password==user.password:
            login_user(user)
            return redirect('/home')
    return render_template('login.html')

@app.route('/home')
def home():
    users = Users.query.all()
    return render_template('home.html',users=users)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        username = request.form['username']
        phoneno = request.form['mobile']
        email = request.form['email']
        password = request.form['password']
        repassword = request.form['repeatpswd']
        address = request.form['address']
        users = Users(username=username,phoneno=phoneno,email=email,password=password,repassword=repassword,address=address)
        db.session.add(users)
        db.session.commit()
        return redirect('/')
    return render_template('register.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

@app.route('/add_contact', methods=['POST','GET'])
def add_contact():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        phoneno = request.form['mobile']
        subject = request.form['subject']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        user = Addcontact(name=name,email=email,phoneno=phoneno,subject=subject,address=address,city=city,state=state)
        db.session.add(user)
        db.session.commit()

    return render_template('add_contact.html')

@app.route('/contact_list')
def contact_list():
    entrys = Addcontact.query.all()
    return render_template('tables.html',entrys = entrys)

@app.route('/edit/<int:id>', methods=['POST','GET'])
def edit(id):
    if request.method=='POST':
        entry = Addcontact.query.filter_by(id=id).first()
        entry.name = request.form.get('name')
        entry.email = request.form.get('email')
        entry.phoneno = request.form.get('mobile')
        entry.subject = request.form.get('subject')
        entry.address = request.form.get('address')
        entry.city = request.form.get('city')
        entry.state = request.form.get('state')
        db.session.commit()
        return redirect('/contact_list')
    return render_template('tables.html')

@app.route('/delete/<int:id>')
def delete(id):
    entry = Addcontact.query.filter_by(id=id).first()
    db.session.delete(entry)
    db.session.commit()
    return redirect('/contact_list')

if __name__ == '__main__':
    app.run(debug=True)