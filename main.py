from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)

screenData = {
    'User': 'Screen 1',
    'URL ngrok': 'https://ngrok.io',
    'switchScreens':{
        'Home': True,
        'Live': False,
        'Game': False
    },
    'Notifications':{
        'askLive':False,
        'Sondage':True,
        'SondageMessage':['Ceci est un sondage test']
        }
}

# Route for the mobile phone
@app.route('/')
def index():
    return render_template("application/index.html")

@app.route('/screenSwitch/<value>', methods=['GET', 'POST'])
def screenSwitch(value):
    if request.method == "GET" and value != None:
        global screenData
        print(screenData['switchScreens']['Live'])
        values = value.split("|")
        print(values[1])
        try:
            if values[0] == 'Live' and values[1] == 'False':
                return screenData, 200
        except:
            print("erreur")
            return 'nop', 200

    else:
        return 'yes', 200

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
