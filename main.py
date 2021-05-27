from flask import Flask, render_template, request, redirect, session, url_for, jsonify

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
    if request.method == "POST" and value != None:
        global screenData
        values = value.split("&")
        try:
            if values[0] == 'Live' and values[1] == 'On':
                screenData['switchScreens']['Live'] = True 
                screenData['switchScreens']['Home'] = False
                return screenData, 200
            if values[0] == 'Live' and values[1] == 'Off':
                screenData['switchScreens']['Live'] = False 
                screenData['switchScreens']['Home'] = True
                return screenData, 200
            else:
                return 'False value', 200
        except:
            print("error")
            return 'Error', 200
    else:
        return screenData, 200

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

if __name__ == '__main__':
    app.run()
