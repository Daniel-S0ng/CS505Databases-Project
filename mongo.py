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

def close_mongo_connection(mongo_client):
    mongo_client.close()
