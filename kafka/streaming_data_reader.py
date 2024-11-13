#!/usr/bin/env python

import os
import mysql.connector

from datetime import datetime
from kafka import KafkaConsumer
from dotenv import load_dotenv


load_dotenv()

TOPIC = 'toll'
HOST = os.environ.get("MYSQL_HOST")
DATABASE = os.environ.get("MYSQL_DB_NAME")
USERNAME = os.environ.get("MYSQL_USERNAME")
PASSWORD = os.environ.get("MYSQL_PASSWORD")

print('Connecting to the database')

try:
    connection = mysql.connector.connect(host=HOST, database=DATABASE, user=USERNAME, password=PASSWORD)
except Exception as e:
    print("Could not connect to database.", e)
else:
    print("Successfully connected to database")

cursor = connection.cursor()

print("Connecting to Kafka")
consumer = KafkaConsumer(TOPIC)
print("Connected to Kafka")
print(f"Reading messages from the topic {TOPIC}")

for msg in consumer:
    # Extract info from kafka
    message = msg.value.decode("utf-8")

    # Transform date format to suit the db schema
    (timestamp, vehicle_id, vehicle_type, plaza_id) = message.split(",")
    
    dateobj = datetime.strptime(timestamp, '%a %b %d %H:%M:%S %Y')
    timestamp = dateobj.strftime("%Y-%m-%d %H:%M:%S")

    # Loading data into the db table
    sql = "INSERT INTO livetolldata values (%s,%s,%s,%s)"
    result = cursor.execute(sql, (timestamp, vehicle_id, vehicle_type, plaza_id))
    print(f"A {vehicle_type} was inserted into the database")
    connection.commit()

connection.close()