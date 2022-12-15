from flask import Flask, render_template

#Create Flask Instance
app = Flask(__name__) #helps flask find filse and directory
app.config['DEBUG'] = True
#Create a route decorator
@app.route('/')

def infex():
    return render_template("index.html")
