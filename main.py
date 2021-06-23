from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_cors import CORS
import json
import requests
import time

from twilio.jwt.access_token import AccessToken
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
    },
    'Notifications':{
        'askLive':'false',
        'Sondage':'true',
        'SondageMessage':['Ceci est un sondage test']
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
@app.route('/api/screenSwitch/<screen>/<value>', methods=['POST'])
def screenSwitch(value, screen):
    if request.method == "POST" and screen != None:
        global screenData
        if screen == 'Live' and value == 'On':
                screenData['switchScreens']['Live'] = 'true' 
                screenData['switchScreens']['Home'] = 'false'
                return screenData, 200
        if screen == 'Live' and value == 'Off':
                screenData['switchScreens']['Live'] = 'false' 
                screenData['switchScreens']['Home'] = 'true'
                return screenData, 200
        else:
            return 'False value', 200


@app.route('/api/screenSwitch/GetData', methods=['GET'])
def screenSwitchGetData():
    return screenData, 200

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

if __name__ == '__main__':
    app.run(#ssl_context=('cert.pem', 'key.pem'), 
    host="0.0.0.0", debug=True, port=5001)
