import os
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask,request,redirect
import requests
from urllib.parse import urlencode

#server link: https://flaskapp-chatbot.herokuapp.com/

app = Flask(__name__)
 
@app.route("/",methods=['GET'])
def reply():
    return "Hello World Updated"

@app.route("/sms",methods=['GET','POST'])
def sms_reply():
    api_key = "e457e8388db343168debe72aa8b2199a"
    incoming_msg = request.values.get('Body', '').lower()

    resp = MessagingResponse() #twilio library

    msg = resp.message()

    def extract_lat_lng(address_or_postalcode):
        endpoint = "https://api.geoapify.com/v1/geocode/search"
        params = {"text": address_or_postalcode, "apiKey": api_key}
        url_params = urlencode(params)
    
        url = f"{endpoint}?{url_params}"
    
        r = requests.get(url)
        if r.status_code not in range(200, 299): 
           return {}
        lat = {}
        lon = {}
        try:
           lat = r.json()['features'][0]['properties']['lat']
           lon = r.json()['features'][0]['properties']['lon']
        except:
          pass
        str_lat = str(lat)
        str_lon = str(lon)
    

        return(str_lat +" "+ str_lon)
    
  
    if incoming_msg[0] == '(':
        msg.body(extract_lat_lng("Andheri, Mumbai"))
     
    if 'service' in incoming_msg:
        msg.body('Enter in the format "(type,location,radius)"')
    
    if 'hello' in incoming_msg:
        msg.body("Hello, this is the NearBy Places Bot \n Type 'service' to get places ")

      

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
