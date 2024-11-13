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


try:
    print(HOST, USERNAME, PASSWORD, DATABASE)
    connection = mysql.connector.connect(host=HOST, database=DATABASE, user=USERNAME, password=PASSWORD)
    print(connection)
except Exception as e:
    print("Could not connect to database.", e)
else:
    print("Successfully connected to database")
