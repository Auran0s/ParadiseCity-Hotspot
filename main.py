from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_cors import CORS
import json
import requests
import time

from twilio.jwt.access_token.grants import VideoGrant, ChatGrant
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

import os
from dotenv import load_dotenv

load_dotenv()
twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')
twilio_client = Client(twilio_api_key_sid, twilio_api_key_secret,
                       twilio_account_sid)

app = Flask(__name__)
CORS(app)

screenData = {
    'User': 'Screen 1',
    'URL ngrok': 'https://ngrok.io',
    'switchScreens':{
        'Home': 'true',
        'Live': 'false',
        'Game': 'false'
    'screensCommands':{
        "screen1":{
            'Home': 'true',
            'Live': 'false',
        },
        "screen2":{
            'Home': 'true',
            'Live': 'false',
        }
    },
    'Notifications':{
        'askLive':'false',
        'Sondage':'true',
        'Sondage':{
            "Message":"",
            "Answer":{
                "oui":12,
                "non":27
            }
        }
    }
}


# Route for the mobile phone
@app.route('/')
def index():
    return render_template("application/index.html")

# App route

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

# Routing API

# Switching screen
@app.route('/api/screen/<screenID>/<action>/<value>', methods=['POST'])
def screenSwitch(screenID, action, value):
    if request.method == "POST" and screenID != None and screenID == '1' or screenID == '2':
        global screenData
        # Switch screen views
        if action == 'Live' and value == 'On' and screenData['screensCommands']['screen'+screenID]['Live'] != 'true':
                screenData['screensCommands']['screen'+screenID]['Live'] = 'true' 
                screenData['screensCommands']['screen'+screenID]['Home'] = 'false'
                screenData['Notifications']['askLive'] = 'true'
                return screenData, 200
        if action == 'Live' and value == 'Off' and screenData['screensCommands']['screen'+screenID]['Live'] != 'false':
                screenData['screensCommands']['screen'+screenID]['Live'] = 'false' 
                screenData['screensCommands']['screen'+screenID]['Home'] = 'true'
                screenData['Notifications']['askLive'] = 'false'
                return screenData, 200
        
        else:
            return {'error messages':'value posted are not the values expected'}, 400
    elif request.method == 'GET' and screenID != None and screenID == '1' or screenID == '2':
        if action == 'getData':
            return screenData, 200
    else:
        return {'error messages':'request or screenID not good'}, 400
    
# Get message
@app.route('/api/messages/<action>', methods=['GET', 'POST'])
def manageMessages(action):
    if request.method == 'GET' and action == 'getData':
        with open("./messages.json", "r") as file:
            data = json.load(file)
            file.close()
        return {'Messages':data}, 200
    elif request.method == 'POST' and action == 'newMessageText':
        newData = request.get_json()
        if newData != None:
            with open("./messages.json", "r+") as file:
                data = json.load(file)
                nbOfMessages = len(data)
                nextId = str(nbOfMessages + 1)
                newMessage ={
                        "id":nextId,
                        "type":"text",
                        "filtre":newData['filtre'],
                        "content":newData['content'],
                    }
                data.append(newMessage)
                file.seek(0)
                json.dump(data, file)
                file.close
        return {'Messages':data}, 200

@app.route('/api/sondage', methods=['GET', 'POST'])
def sondage():
    global screenData 
    sondageData = screenData['Notifications']['Sondage']
    data = request.get_json()
    if request.method == 'GET':
        return sondageData, 200
    elif request.method == 'POST' and data != None:
        if data['data'] == 'oui':
            screenData['Notifications']['Sondage']['Answer']['oui'] = screenData['Notifications']['Sondage']['Answer']['oui'] + 1
            return {'Message':'Vote taken [Oui]'}, 200
        elif data['data'] == 'non':
            screenData['Notifications']['Sondage']['Answer']['non'] = screenData['Notifications']['Sondage']['Answer']['non'] + 1
            return {'Message':'Vote taken [Non]'}, 200
    else:
        return {'error message': 'bad request'}, 400
        

if __name__ == '__main__':
    app.run(#ssl_context=('cert.pem', 'key.pem'), 
    host="0.0.0.0", debug=True, port=5001)
