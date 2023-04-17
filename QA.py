from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import BooleanField, DecimalField, TextAreaField, validators
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask_mysqldb import MySQL
#import mysql
import mysql.connector
import pymysql
from datetime import date
from flask import session

#Connection
mydb=mysql.connector.connect(host='localhost', user='root', passwd='password123', database='qa_test') #define database
cur = mydb.cursor()


#test
#cur.execute("show tables in qa_test")
#for i in cur:
#    print(i)


#Create Flask Instance
app = Flask(__name__) #helps flask find filse and directory
app.config['SECRET_KEY'] = "Super key" #CSRF
#with app.app_context():
#    db.create_all()

##############################################

class DataStore():
    select = None

data = DataStore()


#Create Form Classes
class DailyQAForm1(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    gantry = IntegerField("Gantry: ", validators=[DataRequired(), NumberRange(min=1, max=4, message='Invalid')])
    laserx = BooleanField("Laser x axis: ")
    lasery = BooleanField("| Laser y axis: ")
    laserz = BooleanField("| Laser z axis: ")
    temperature = DecimalField("Temperature [°C]:", validators=[DataRequired()])
    pressure = DecimalField("Pressure [hPa]:", validators=[DataRequired()])

    submit = SubmitField("Submit")

class DailyQAForm2(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    gantry = IntegerField("Gantry: ", validators=[DataRequired(), NumberRange(min=1, max=4, message='Invalid')])
    laserx = BooleanField("Laser x axis: ")
    lasery = BooleanField("| Laser y axis: ")
    laserz = BooleanField("| Laser z axis: ")
    temperature = DecimalField("Temperature [°C]:", validators=[DataRequired()])
    pressure = DecimalField("Pressure [hPa]:", validators=[DataRequired()])

    submit = SubmitField("Submit")


#############################################

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



#Create dailyQA form page
@app.route('/daily', methods = ['GET', 'POST'])
def daily():

    return render_template("daily.html")

    #print(request.args.get('gantry_select'))
    #print(type(request.form['gantry_select']))

@app.route("/daily/test" , methods=['GET', 'POST'])
def test():
    
    select = str(request.form.get('gantry_select'))
    if select == 'FBTR1':
        form = DailyQAForm1()
    elif select == 'GTR2':
        form = DailyQAForm2()
    elif select == 'GTR3':
        form = DailyQAForm3()
    elif select == 'GTR4':
        form = DailyQAForm4()

    print(select)
    print(select == 'FBTR1')
    lastChar = select[-1]
    print("daily" + lastChar + ".html")
    #variables
    name = None
    gantry = 0
    laserx = 0
    lasery=0
    laserz=0
    temperature=0
    pressure=0

    #Validate
    if form.validate_on_submit():
        #name = daily_test(form.name.data)
        #gantry = daily_test(form.gantry.data)
        name = form.name.data
        laserx = form.laserx.data
        lasery = form.lasery.data
        laserz = form.laserz.data
        if form.laserx.data == True: laserx = 1
        if form.lasery.data == True: lasery = 2
        if form.laserz.data == True: laserz = 4
        lasers = laserx + lasery + laserz

        gantry = int(form.gantry.data)
        temperature = form.temperature.data
        pressure = form.pressure.data
        
        #cur.execute("INSERT INTO qa_test (daily_test) VALUES (%s)", (gantry))
        cur.execute("INSERT INTO qa_test.daily_test (Date_added, Gantry, Lasers, Temperature, Pressure) VALUES (%s, %s, %s, %s, %s)", (datetime.now(), gantry, lasers, temperature, pressure))
        mydb.commit()
        cur.close()

        #mydb.session.add(name,gantry)
        #mydb.session.commit()
        
        #form.name.data = ''
        #form.gantry.data = ''

        #return "Success"

    return render_template("daily" + select[-1] + ".html", 
        form=form) #do I need other variables?





