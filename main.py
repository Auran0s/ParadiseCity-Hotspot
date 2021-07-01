from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from flask_cors import CORS, cross_origin
import json
import requests
import time

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
cors = CORS(app)

screenData = {
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
        'askLive':'false'
    },
    'Sondage':{
        'SondageState':'true',
        "Message":"Aimez-vous les pizzas à l'ananas ?",
        "Answer":{
            "oui":12,
            "non":27
        }
    }
}


# Route for the screen
@app.route('/')
def home():
   return render_template("/index.html")

@app.route('/livescreen')
def livescreen():
    return render_template("/livescreen.html")

# Routing API

@app.route('/api/getData', methods=['GET'])
def getData():
    if request.method == 'GET':
        return screenData, 200
    else:
        return {'error messages':'request or screenID not good'}, 400


# Switching screen
@app.route('/api/screen/<screenID>/<action>/<value>', methods=['POST'])
def screenSwitch(screenID, action, value):
    if request.method == "POST" and screenID != None and screenID == '1' or screenID == '2':
        print(screenID, action, value)
        global screenData
        print(screenData)
        # Switch screen views
        if action == 'Live' and value == 'On' and screenData['screensCommands']['screen'+screenID]['Live'] != 'true':
                screenData['screensCommands']['screen'+screenID]['Live'] = 'true' 
                screenData['screensCommands']['screen'+screenID]['Home'] = 'false'
                screenData['Notifications']['askLive'] = 'true'
                return screenData, 200
        elif action == 'Live' and value == 'Off':
                screenData['screensCommands']['screen1']['Live'] = 'false'
                screenData['screensCommands']['screen1']['Home'] = 'true'
                screenData['screensCommands']['screen2']['Live'] = 'false'
                screenData['screensCommands']['screen2']['Home'] = 'true'
                screenData['Notifications']['askLive'] = 'false'
                return screenData, 200
        else:
            return {'error messages':'value posted are not the values expected'}, 400
    
# Get message
@app.route('/api/messages/<action>', methods=['GET', 'POST'])
def manageMessages(action):
    if request.method == 'GET' and action == 'getData':
        with open("./messages.json", "r") as file:
            data = json.load(file)
            nbOfMessages = len(data)
            if nbOfMessages > 12:
                lastMessage = nbOfMessages - 12
                file.close()
                return {'Messages':data[lastMessage:nbOfMessages]}, 200
            else:
                file.close()
                return {'Messages':data[0:11]}, 200 
    elif request.method == 'POST' and action == 'newMessageText':
        newData = request.get_json()
        if newData != None:
            listContent = list(newData['content'])
            if len(listContent) >= 250:
                print(len(listContent))
                splitContent = ''.join(listContent[0:250]) + ' ...'
            else:
                splitContent = newData['content']
            with open("./messages.json", "r+") as file:
                data = json.load(file)
                nbOfMessages = len(data)
                nextId = str(nbOfMessages + 1)
                newMessage ={
                        "id":nextId,
                        "type":"text",
                        "filtre":newData['filtre'],
                        "split_content": splitContent,
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
    sondageData = screenData['Sondage']
    data = request.get_json()
    if request.method == 'GET':
        return sondageData, 200
    elif request.method == 'POST' and data != None:
        if data['data'] == 'oui':
            screenData['Sondage']['Answer']['oui'] = screenData['Sondage']['Answer']['oui'] + 1
            return {'Message':'Vote taken [Oui]'}, 200
        elif data['data'] == 'non':
            screenData['Sondage']['Answer']['non'] = screenData['Sondage']['Answer']['non'] + 1
            return {'Message':'Vote taken [Non]'}, 200
    else:
        return {'error message': 'bad request'}, 400

@app.route('/api/notifications', methods=['GET'])
def notifications():
    global screenData
    return {'Notification': screenData['Notifications']}
        

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), 
    host="0.0.0.0", debug=True, port=5001)
