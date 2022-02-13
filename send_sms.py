import os
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask,request,redirect
import requests

app = Flask(__name__)


@app.route("/sms",methods=['GET','POST'])
def sms_reply():
    incoming_msg = request.values.get('Body', '').lower()

    resp = MessagingResponse()

    msg = resp.message()

    if 'hi' in incoming_msg:
        msg.body("Hello i am a bot created today")

    if 'hello' in incoming_msg:
        msg.body("Great Success!")    

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)