import threading
from flask import Flask, render_template, request, jsonify
import json
from Subscriber import run_subscriber

from mongo import mongo_connection, close_mongo_connection

app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
def hello_world():
    
    return ("<p>Hello, World!</p>")

@app.route("/api/getteam", methods=['GET','POST'])
def getteam():
    #to address MF1 in the assignment
    response = { "team_name": "Daniel and Sandesh",
    "members": ["912333054", "912270286"],
    "app_status_code": 1,
    }
    return (render_template('getteam.html',
                            project_status=jsonify(response)))

# @app.route('/api/getteam', methods=['GET'])
# def get_team():
#     response = { "team_name": "Daniel and Sandesh",
#     "members": ["912333054", "912270286"],
#     "app_status_code": 1,
#     }
#     return (render_template('getteam.html',
#                             project_status=jsonify(response)), jsonify(response))

@app.route("/api/reset", methods=['GET','POST'])
def reset():
    #To address MF2 in the assignment
    # code 0 = my data could not be reset, 1 = my data was reset
    #TODO: change this when resetting is implemented
    isReset = 0
    response = {"reset_status_code":isReset}
    return(render_template('reset.html',reset_status = jsonify(response)), jsonify(response))

@app.route("/api/zipalertlist")
def zipalertlist():
    #To address RTR1 in the assignment
    #TODO: have this call a function in the controller which returns the list of zip codes
    
    response = {"ziplist": [40351,40513,40506]}

    return (render_template('zipalertlist.html', ziplist = jsonify(response)), jsonify(response))

@app.route("/api/alertlist")
def alertlist():
    #To address RTR2 in the assignment
    #code 0 = state is not in alert, 1 = state is in alert
    #TODO: have this call a function in the controller which decides if a state is in alert or not

    response = {"state_status": 0}

    return (render_template('alertlist.html', state_status = jsonify(response)), jsonify(response))

@app.route("/api/getconfirmedcontacts/<mrn>")
def confirmedcontacts(mrn):
    #To address CT1 in the assignment
    #TODO: have this call a function in the controller which returns list of patient_mrn 
    #       that have been in direct contact with the provided {mrn}

    response = {"contactlist": [121345,54321,86754]}

    return (render_template('confirmedcontacts.html', contactlist = jsonify(response)), jsonify(response))

@app.route("/api/getpossiblecontacts/<mrn>")
def possiblecontacts(mrn):
    #To address CT2 in the assignment
    #TODO: have this call a function in the controller which 
    #       returns list of events with list of patient_mrn that have might have been in direct contact with the provided {mrn}

    response = {"contactlist": '[001:[121345,5431],002:[54321,56344],003:[86754,12345]]'}

    return (render_template('possiblecontacts.html', possiblecontactlist = jsonify(response)), jsonify(response))

@app.route("/api/getpatientstatus/<hospital_id>")
def patientStatusByHospitalId(hospital_id):
    #To address OF1 in the assignment
    #TODO: have this call a function in the controller which 
    #       returns list of events with list of patient_mrn that have might have been in direct contact with the provided {mrn}

    response = {"in-patient_count": 78,
                        "in-patient_vax": 0.41,
                        "icu-patient_count": 11,
                        "icu_patient_vax": 0.18, 
                        "patient_vent_count": 6,
                        "patient_vent_vax": 0.17
                        }

    return (render_template('patientStatusByHospitalId.html', patient_status = jsonify(response)), jsonify(response))

@app.route("/api/getpatientstatus/")
def patientstatus():
    #To address OF2 in the assignment
    #TODO: have this call a nction in the controller which returns counts for 
    # in-patients, icu patients, and patients on ventilators, along with percentage vaccinated

    response = { "in-patient_count": 178,
                       "in-patient_vax": 0.31,
                       "icu-patient_count": 78,
                       "icu_patient_vax": 0.19, 
                       "patient_vent_count": 25,
                       "patient_vent_vax": 0.12 }
    
    return (render_template('patientstatus.html', patient_status = jsonify(response)), jsonify(response))

if __name__ == '__main__':
    subscriber_thread = threading.Thread(target=run_subscriber)
    subscriber_thread.start()
    app.run(host="0.0.0.0", port=9999, debug=True)