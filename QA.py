from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

#Create Flask Instance
app = Flask(__name__) #helps flask find filse and directory
#SQLite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password123@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = "Super Key"

#Initialize database
db = SQLAlchemy(app)

#Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True) #keep track of users
    name = db.Column(db.String(120), nullable=False) #can't be blank
    email = db.Column(db.String(120), nullable=False, unique=True) #unique email
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create a string
    def __repr__(self):     
        return '<Name %r>' % self.name

with app.app_context():
    db.create_all()

#Create a route decorator
@app.route('/') #homepage
def index():
    return render_template("index.html")

#Create a Form Class
class NameForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    email = StringField("Email: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/users', methods=['GET', 'POST'])
def users():
    name = None
    email = None
    form = NameForm()
    #Validate
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("Form Submitted Succesfully")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("users.html", 
    name = name,
    form = form, 
    our_users=our_users)

#Update database record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = NameForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try: 
            db.session.commit()
            flash("User Updated")
            return render_template("update.html", 
            form=form,
            name_to_update=name_to_update)
        except:
            flash("Problem")
            return render_template("update.html", 
            form=form,
            name_to_update=name_to_update)
    else:
        return render_template("update.html", 
            form=form,
            name_to_update=name_to_update)

