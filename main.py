from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)

screenCommandes = {
    'liveOn': False
}

# Route for the mobile phone
@app.route('/')
def index():
    return render_template("application/index.html")

@app.route('/screenSwitch/<value>', methods=['GET', 'POST'])
def screenSwitch(value):
    if request.method == "POST" and value == "liveOn":
        global screenCommandes
        screenCommandes = {value: True}
        print(screenCommandes)
        return screenCommandes, 200
    else:
        return screenCommandes, 200

@app.route('/livecontrol')
def liveControl():
    return render_template("application/livecontrol.html")

# Route for the screen

@app.route('/home')
def home():
   return render_template("screen/index.html")

@app.route('/livescreen')
def livescreen():
   return render_template("screen/livescreen.html")
