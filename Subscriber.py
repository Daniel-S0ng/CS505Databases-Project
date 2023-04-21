# subscriber.py

import time
import pika
import sys
import json
import mongo

# Set the connection parameters to connect to rabbit-server1 on port 5672
username = 'team_11'
password = 'myPassCS505'
hostname = 'vbu231.cs.uky.edu'
virtualhost = '11'
port = 9099

# Set up MongoDB
mongo_client = mongo.mongo_connection()

def callback(ch, method, properties, body):
    data = json.loads(body)
    
    if method.exchange == "patient_list":
        mongo.insert_testing_data(data)

    elif method.exchange == "hospital_list":
        mongo.insert_hospital_data(data)

    elif method.exchange == "vax_list":
        mongo.insert_vaccination_data(data)

#This method is only created to test mongodb, can be removed after rabbitMQ is back.
def testCallBack(topic, message):
    data = json.loads(message)
    
    if topic == "patient_list":
        mongo.insert_testing_data(data)

    elif topic == "hospital_list":
        mongo.insert_hospital_data(data)

    elif topic == "vax_list":
        mongo.insert_vaccination_data(data)

def generate_test_data():
    return json.dumps([{
        "testing_id": 1,
        "patient_name": "Lebron James",
        "patient_mrn": "024c60d2-a1eb",
        "patient_zipcode": 40351,
        "patient_status": 1,
        "contact_list": ["498d-8739", "0d2-a1eb-498"],
        "event_list": ["234fs-3493", "fsf545-dfs54"]
    }])

def generate_hospital_data():
    return json.dumps([{
        "hospital_id": 2,
        "patient_name": "Daniel Song",
        "patient_mrn": "024c60d2-a1eb",
        "patient_status": 3
    }])

def generate_vax_data():
    return json.dumps([{
        "vaccination_id": 2,
        "patient_name": "Sandesh Lamichhane",
        "patient_mrn": "024c60d2-a1eb",
    }])

def run_subscriber():
    while True:
        time.sleep(1)  # Simulate a delay between messages

        # Simulate receiving a testing data message
        testing_data = generate_test_data()
        testCallBack("patient_list", testing_data)

        time.sleep(1)

        # Simulate receiving a hospital data message
        hospital_data = generate_hospital_data()
        testCallBack("hospital_list", hospital_data)

        time.sleep(1)

        # Simulate receiving a vaccination data message
        vax_data = generate_vax_data()
        testCallBack("vax_list", vax_data)
        
# def run_subscriber():
#     credentials = pika.PlainCredentials(username, password)
#     parameters = pika.ConnectionParameters(hostname, port, virtualhost, credentials)
#     try:
#         connection = pika.BlockingConnection(parameters)
#         print("Successfully connected to the RabbitMQ server")
#     except pika.exceptions.AMQPConnectionError as error:
#         print("Failed to connect to the RabbitMQ server:", error)
#         return
#     channel = connection.channel()
#     binding_keys = "#"
#     result = channel.queue_declare('', exclusive=True)
#     queue_name = result.method.queue

#     for binding_key in binding_keys:
#         for ex in ['patient_list', 'hospital_list', 'vax_list']:
#             channel.exchange_declare(exchange=ex, exchange_type='topic')
#             channel.queue_bind(
#                 exchange=ex, queue=queue_name, routing_key=binding_key)

#     channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
#     channel.start_consuming()

#     close_sqlite_connection(sqlite_conn)
#     close_mongo_connection(mongo_client)
