from flask import Flask, abort, jsonify, request
import requests
import json

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def makeRequest():
    data = request.get_json(force=True)

    base_url="https://testflight2.via.com/apiv2"
    heeaders = {'Content-Type': 'application/json'}

    payload = ' { "sectorInfos":[ { "src":{ "code": "'+ data['source'] + '" }, "dest":{ "code":"' + data['distination'] + '"}, "date":"'+ data['date'] + '" } ], "class":"ALL", "paxCount":{ "adt":"'+ data['adult'] + '", "chd":0, "inf":"0" }, "route":"ALL" }'

    response = requests.post("https://testflight2.via.com/apiv2/flight/search", headers = heeaders, data=payload)


    jouney_dict = json.loads(response.text)

    allflight = []


    for flight in range (len(jouney_dict['onwardJourneys'])):
        
        newFlightDict = {}

        newFlightDict.update({"fare": jouney_dict['onwardJourneys'][flight]["fares"]["totalFare"]["total"]["amount"]})
    
        singleFlightList = []
    
    
        for item in range (len(jouney_dict['onwardJourneys'][flight]["flights"])):
        
            singleFlight = {}

            

            flNo =  jouney_dict['onwardJourneys'][flight]["flights"][item]["carrier"]["code"] + " " + jouney_dict['onwardJourneys'][flight]["flights"][item]["flightNo"]

            singleFlight.update({"key" : jouney_dict['onwardJourneys'][flight]["flights"][item]["key"] })
            singleFlight.update({"carrierName" : jouney_dict['onwardJourneys'][flight]["flights"][item]["carrier"]["name"] })
            singleFlight.update({"departCity" : jouney_dict['onwardJourneys'][flight]["flights"][item]["depDetail"]["name"] })
            singleFlight.update({"departTime" : jouney_dict['onwardJourneys'][flight]["flights"][item]["depDetail"]["time"] })
            singleFlight.update({"arrivalCity" : jouney_dict['onwardJourneys'][flight]["flights"][item]["arrDetail"]["name"]  })
            singleFlight.update({"arrivalTime" : jouney_dict['onwardJourneys'][flight]["flights"][item]["arrDetail"]["time"] })
            singleFlight.update({"flightNo" : flNo})
            singleFlight.update({"flightDuration" : jouney_dict['onwardJourneys'][flight]["flights"][item]["flyTime"] }) 
            singleFlight.update({"flightLayover" : jouney_dict['onwardJourneys'][flight]["flights"][item].get("layover") })
            singleFlight.update({"flightClass" : jouney_dict['onwardJourneys'][flight]["flights"][item].get("cabinClass") })
            singleFlight.update({"flightRefundable": jouney_dict['onwardJourneys'][flight]["flights"][item].get("refundable") })     

            singleFlightList.append(singleFlight)

        newFlightDict.update({"flightList":singleFlightList})
       
        allflight.append(newFlightDict)


    return jsonify(allflight)


if __name__ == '__main__':
    app.run(debug = True)