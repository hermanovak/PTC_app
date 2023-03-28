from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_mysqldb import MySQL
import mysql.connector
import pymysql

#Connection
mydb=mysql.connector.connect(host='localhost', user='root', passwd='password123')
cur = mydb.cursor()

#test
#cur.execute("show tables in qa_test")
#for i in cur:
#    print(i)


#Create Flask Instance
app = Flask(__name__) #helps flask find filse and directory

#with app.app_context():
#    db.create_all()

#Create a route decorator
@app.route('/', methods = ['GET', 'POST']) #homepage
def index():
    return render_template("index.html")

#Create a route decorator

@app.route('/weekly', methods = ['GET', 'POST']) #weekly test
def weekly():
    return render_template("weekly.html")

@app.route('/monthly', methods = ['GET', 'POST']) #monthly test
def monthly():
    return render_template("monthly.html")

##############################################

#Create a Form Class
class DailyQAForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    gantry = StringField("Gantry: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

#Create dailyQA form page
@app.route('/daily', methods = ['GET', 'POST'])
def daily():
    name = None
    gantry = None
    #form = DailyQAForm()
    form = request.form
    #Validate
    if form.validate_on_submit():
        #name = daily_test(form.name.data)
        #gantry = daily_test(form.gantry.data)
        name = form['name']
        gantry = form['gantry']
        cur.execute("INSERT INTO daily_test(Gantry) VALUES (%s, %s)", (gantry))
        db.connection.commit()
        cur.close()

        #db.session.add(name,gantry)
        #db.session.commit()
        
        #form.name.data = ''
        #form.gantry.data = ''

        return "Success"


    return render_template("daily.html", 
        name = name,
        gantry=gantry,
        form=form)



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

