from functools import wraps
import threading
from flask import Flask, make_response, render_template, request, jsonify
import json
from Subscriber import run_subscriber
import mongo

app = Flask(__name__)
# If 0, use mongoDb, If 1, use **.
database_type = 0

def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response

    return no_cache

@app.route("/", methods=['GET','POST'])
def hello_world():
    
    return ("<p>Hello, World!</p>")

# @app.route("/api/getteam", methods=['GET','POST'])
# def getteam():
#     #to address MF1 in the assignment
#     response = { "team_name": "Daniel and Sandesh",
#     "members": ["912333054", "912270286"],
#     "app_status_code": 1,
#     }s
#     return (render_template('getteam.html',
#                             project_status=jsonify(response)))

@app.route('/api/getteam', methods=['GET'])
def get_team():
    response = { "team_name": "Daniel and Sandesh",
    "members": ["912333054", "912270286"],
    "app_status_code": 1,
    }
    return jsonify(response)

@app.route("/api/reset", methods=['GET','POST'])
def reset():
    #To address MF2 in the assignment
    # code 0 = my data could not be reset, 1 = my data was reset
    #TODO: change this when resetting is implemented
    #reset
    try:
        mongo.reset_data_mongodb()
        response = {"reset_status_code": 1}
    except Exception as e:
        response = {"reset_status_code": 0}
    
    return jsonify(response)
    
@app.route("/api/zipalertlist")
def zipalertlist():
    #To address RTR1 in the assignment
    #TODO: have this call a function in the controller which returns the list of zip codes
    alert_zipcodes = mongo.get_alert_zipcodes()
    response = {"ziplist": [alert_zipcodes]}
    return jsonify(response)

@app.route("/api/alertlist")
def alertlist():
    #To address RTR2 in the assignment
    #code 0 = state is not in alert, 1 = state is in alert
    #TODO: have this call a function in the controller which decides if a state is in alert or not

    response = {"state_status": 0}
    return jsonify(response)

@app.route("/api/getconfirmedcontacts/<mrn>")
def confirmedcontacts(mrn):
    #To address CT1 in the assignment
    #TODO: have this call a function in the controller which returns list of patient_mrn 
    #       that have been in direct contact with the provided {mrn}

    return mongo.getConfirmedContacts(mrn)

@app.route("/api/getpossiblecontacts/<mrn>")
def possiblecontacts(mrn):
    #To address CT2 in the assignment
    #TODO: have this call a function in the controller which 
    #       returns list of events with list of patient_mrn that have might have been in direct contact with the provided {mrn}

    return mongo.getpossiblecontacts(mrn)

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
    return jsonify(response)

@app.route("/api/getpatientstatus/", methods=["GET"], defaults={'hospital_id': None})
@app.route("/api/getpatientstatus/<int:hospital_id>", methods=["GET"])
@nocache
def patientstatus(hospital_id=None):
    #To address OF2 in the assignment
    #TODO: have this call a nction in the controller which returns counts for 
    # in-patients, icu patients, and patients on ventilators, along with percentage vaccinated

    return mongo.getpatientstatus(hospital_id)



if __name__ == '__main__':
    subscriber_thread = threading.Thread(target=run_subscriber)
    subscriber_thread.start()
    app.run(host="0.0.0.0", port=9999, debug=True)