import os
from unicodedata import category
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

    def extract_lat_lng(address_or_postalcode): #getting lat long function
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
        return lat,lon

    def extract_details(lat_lng,category,radius=3000):
    
        if (category =="hospital"):
            cat = "healthcare.hospital"
        elif (category == "supermarket"):
            cat = "commercial"
        elif (category == "restuarant"):
            cat = "catering"
        else:
            return "Invalid Input"
    
    
        endpoint2 = "https://api.geoapify.com/v2/places"
        bias_str = f"proximity:{lat_lng[1]},{lat_lng[0]}"
    
        params2 = {"categories": cat, "filter":f"circle:{lat_lng[1]},{lat_lng[0]},{radius}", "bias":bias_str, "limit":10, "apiKey": api_key}
        url_params2 = urlencode(params2)
        url2 = f"{endpoint2}?{url_params2}"
        
        r = requests.get(url2)
        if r.status_code not in range(200, 299): 
            return {}
    
        names_dict = {} 
        try:
            for i in range (0,10):
                name = r.json()['features'][i]['properties']['name']
                address = r.json()['features'][i]['properties']['formatted']
                names_dict.update({name:address})
        except:
            pass
    
        return names_dict
  
    if incoming_msg[0] == '(':
        incoming_msg = incoming_msg[1:-1]
        stringlist = incoming_msg.split(",",2)
        category = stringlist[0]
        radius = stringlist[1]
        location = stringlist[2]     
        lat_lng = extract_lat_lng(location)
        res = extract_details(lat_lng,category,radius)
        outputstring = ""
        name = list(res.keys())
        address = list(res.values())
        try:
            for i in range(0,10):
                outputstring = outputstring + "Name: " + name[i] + "\nAddress: " + address[i] + "\n\n"
        except: 
            pass
        msg.body(outputstring)
     
    if 'service' in incoming_msg:
        msg.body('Enter in the format "(type,radius,location)"')
    
    if 'hello' in incoming_msg:
        msg.body("Hello, this is the NearBy Places Bot \n Type 'service' to get places ")

      

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
