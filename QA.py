from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

#Create Flask Instance
app = Flask(__name__) #helps flask find filse and directory
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
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
    submit = SubmitField("Submit")

@app.route('/users', methods=['GET', 'POST'])
def users():
    name = None
    form = NameForm()
    #Validate
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Succesfully")

    return render_template("users.html", 
    name = name,
    form = form)
