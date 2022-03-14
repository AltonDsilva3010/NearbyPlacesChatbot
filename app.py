import os
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask,request,redirect
import requests

app = Flask(__name__)

@app.route("/",methods=['GET'])
def reply():
    return "Hello World Updated"

@app.route("/sms",methods=['GET','POST'])
def sms_reply():
    incoming_msg = request.values.get('Body', '').lower()

    resp = MessagingResponse() #twilio library

    msg = resp.message()

    if incoming_msg[0] == '(':
        msg.body(incoming_msg[1::])
     
    if incoming_msg is 'service':
        msg.body('Enter in the format "(type,location,radius)"')
    
    if 'hello' in incoming_msg:
        msg.body("Hello, this is the NearBy Places Bot \n Type 'service' to get places ")

      

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
