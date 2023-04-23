from flask import jsonify
import pymongo

def mongo_connection():
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    mongo_db = mongo_client["covid_data"]
    return mongo_db

def insert_testing_data(testing_data):
    mongo_db = mongo_connection()
    testing_collection = mongo_db["testing_data"]
    testing_collection.insert_many(testing_data)

def insert_vaccination_data(vaccination_data):
    mongo_db = mongo_connection()
    vaccination_collection = mongo_db["vaccination_data"]
    vaccination_collection.insert_many(vaccination_data)

def insert_hospital_data(hospital_data):
    mongo_db = mongo_connection()
    hospital_collection = mongo_db["hospital_data"]
    hospital_collection.insert_many(hospital_data)

# for MF2
def reset_data_mongodb():
    mongo_db = mongo_connection()
    
    # Drop the collections
    mongo_db["testing_data"].drop()
    mongo_db["vaccination_data"].drop()
    mongo_db["hospital_data"].drop()

# for RTR1 ??
def get_alert_zipcodes():
    mongo_db = mongo_connection()
    testing_collection = mongo_db["testing_data"]

    # Find unique zip codes in the collection
    unique_zipcodes = testing_collection.distinct("patient_zipcode")
    alert_zipcodes = []

    for zipcode in unique_zipcodes:
        # Find testing data for the current zip code and sort by batch_number
        zipcode_data = list(testing_collection.find({"zipcode": zipcode}).sort("batch_number"))

        for i in range(len(zipcode_data) - 2):
            m0 = zipcode_data[i]["positive_tests"]
            m1 = zipcode_data[i + 1]["positive_tests"]
            m2 = zipcode_data[i + 2]["positive_tests"]

            if m1 >= 2 * m0 and m2 < 2 * m1:
                alert_zipcodes.append(zipcode)
                break

    return alert_zipcodes

def getConfirmedContacts(mrn):
    mongo_db = mongo_connection()
    testing_collection = mongo_db["testing_data"]
    results = testing_collection.find({"contact_list": {"$elemMatch": {"$regex": mrn, "$options": "i"}}})

    contact_list = []
    for result in results:
        if 'patient_mrn' in result:
            contact_list.append(result['patient_mrn'])

    return jsonify({"contactlist": contact_list})

def getpossiblecontacts(mrn):
    mongo_db = mongo_connection()
    testing_collection = mongo_db["testing_data"]

    pipeline = [
            {"$match": {"patient_mrn": mrn}},
            {"$unwind": "$event_list"},
            {"$group": {"_id": "$event_list"}},
            {"$lookup": {
                "from": "testing_data",
                "localField": "_id",
                "foreignField": "event_list",
                "as": "related_patients"
            }},
            {"$unwind": "$related_patients"},
            # if want to include the person himself, comment out this line.
            {"$match": {"related_patients.patient_mrn": {"$ne": mrn}}},
            {"$group": {"_id": "$_id", "patient_mrns": {"$addToSet": "$related_patients.patient_mrn"}}}
        ]
    related_patients = list(testing_collection.aggregate(pipeline))

    # Convert the output to the desired format
    output = {"contactlist": [{event["_id"]: event["patient_mrns"]} for event in related_patients]}
    return jsonify(output)

def getpatientstatus(hospitalId=None):
    mongo_db = mongo_connection()
    testing_collection = mongo_db["testing_data"]
    hospital_collection = mongo_db["hospital_data"]
    vaccination_collection = mongo_db["vaccination_data"]
    
    if hospitalId is None:
        collection = hospital_collection.find()
    else:
        collection = hospital_collection.find({"hospital_id": hospitalId})
 
    hospital_json = [record for record in collection]
    
    # Converting ObjectId to str for JSON serialization
    for record in hospital_json:
        record["_id"] = str(record["_id"])


    in_patient_list = list({record["patient_mrn"]: record for record in hospital_json if record["patient_status"] == 1}.values())
    in_patient_count = len(in_patient_list)

    icu_patient_list = list({record["patient_mrn"]: record for record in hospital_json if record["patient_status"] == 2}.values())
    icu_patient_count = len(icu_patient_list)

    vent_patient_list = list({record["patient_mrn"]: record for record in hospital_json if record["patient_status"] == 3}.values())
    vent_patient_count = len(vent_patient_list)
    
    in_patient_mrn_list = [record["patient_mrn"] for record in in_patient_list]
    in_patient_vax_count = vaccination_collection.count_documents({"patient_mrn": {"$in": in_patient_mrn_list}})

    icu_patient_mrn_list = [record["patient_mrn"] for record in icu_patient_list]
    icu_patient_vax_count = vaccination_collection.count_documents({"patient_mrn": {"$in": icu_patient_mrn_list}})

    vent_patient_mrn_list = [record["patient_mrn"] for record in vent_patient_list]
    vent_patient_vax_count = vaccination_collection.count_documents({"patient_mrn": {"$in": vent_patient_mrn_list}})

    output = {
        "in-patient_count": in_patient_count,
        "in-patient_vax": in_patient_vax_count/in_patient_count,
        "icu-patient_count": icu_patient_count,
        "icu_patient_vax": icu_patient_vax_count/icu_patient_count,
        "patient_vent_count": vent_patient_count,
        "patient_vent_vax": vent_patient_vax_count/vent_patient_count
    }

    return output




def get_state_alert_status():
    alert_zipcodes = get_alert_zipcodes()

    if len(alert_zipcodes) >= 5:
        return 1
    else:
        return 0

def close_mongo_connection(mongo_client):
    mongo_client.close()

