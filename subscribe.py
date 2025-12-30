import paho.mqtt.client as mqtt
import json
import mysql.connector
import random
import datetime

# MySQL configuration
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Agarwal54321'
MYSQL_DB = 'gps_data'

# Establish MySQL connection
mysql_connection = mysql.connector.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB
)
mysql_cursor = mysql_connection.cursor()

# MQTT Broker details
MQTTBROKER = 'test.mosquitto.org'
PORT = 1883

serial_number = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("gps_data")

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code " + str(rc))

def on_message(client, userdata, msg):
    global serial_number
    serial_number += 1

    print(MQTTBROKER + ': <' + msg.topic + "> : " +  str(msg.payload.decode()))

    message = msg.payload.decode()
    topic = msg.topic

    try:
        message_data = json.loads(message)
        if isinstance(message_data, dict):
            latitude = message_data.get("latitude", 0.0)
            longitude = message_data.get("longitude", 0.0)
            temperature = message_data.get("temperature", 0.0)
            robid = message_data.get("robid", 0.0)
            quality_1 = message_data.get("quality_1", 0.0)
            quality_2 = message_data.get("quality_2", 0.0)
            quality_3 = message_data.get("quality_3", 0.0)
            data_id = message_data.get("data_id", 0.0)

            # Get current date and time
            current_time = datetime.datetime.now()
            date = current_time.date()
            time = current_time.time()

        else:
            raise ValueError("Invalid message format: message_data is not a dictionary")
    except (json.JSONDecodeError, ValueError) as e:
        print("Failed to parse message as JSON:", str(e))
        return

    insert_query = "INSERT INTO gps_data (serial_number, robot_id, topic, temperature, latitude, longitude, quality_1, quality_2, quality_3, data_id, date, time) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)"
    insert_values = (serial_number, robid, topic, temperature, latitude, longitude, quality_1, quality_2, quality_3, data_id, date, time)
    
    mysql_cursor.execute(insert_query, insert_values)
    mysql_connection.commit()      

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTTBROKER, PORT)
client.loop_forever()

mysql_cursor.close()
mysql_connection.close()
