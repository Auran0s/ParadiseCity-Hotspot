from flask import Flask, render_template, request, redirect, session

app = Flask(__name__) 

message = "okay"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/screenSwitch', methods=['GET', 'POST'])
def screenSwitch():
    if request.method == "POST":
       return message, 200
    else:
        return "get"