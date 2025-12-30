import paho.mqtt.client as mqtt
import numpy as np
import time
import json
import random
import datetime
import string
# current_time = datetime.datetime.now()
MQTTBROKER = 'test.mosquitto.org'
PORT = 1883
TOPIC = "gps_data"
mqttc = mqtt.Client()
mqttc.connect(MQTTBROKER, PORT)
#  a=0 
def generate_unique_data_id():
    letter = random.choice(string.ascii_lowercase)
    number = random.randint(10, 99)
    return f"data_{letter}{number}"
while True:
    current_time = datetime.datetime.now()
    serial_number_str = datetime.datetime.now()
    serial_number = serial_number_str.strftime("%Y-%m-%d %H:%M:%S")
    latitude = np.random.uniform(25.45, 25.12)
    longitude = np.random.uniform(82.80, 83.23)
    temperature = np.random.uniform(34, 40)
    quality_1 = np.random.uniform(1, 100)
    quality_2 = np.random.uniform(1, 100)
    quality_3 = np.random.uniform(1, 100)
    randid = random.randint(1, 5)
    robid = "id"+str(randid)
    data_id = generate_unique_data_id()
    date = current_time.date().strftime("%Y-%m-%d")
    Time = current_time.time().strftime("%H:%M:%S")

        # for inrange(1,5)
        #     for inrange(1,48)

    message = json.dumps({
        "serial_number": serial_number,
        "latitude": latitude,
        "longitude": longitude,
        "temperature": temperature,
        "quality_1": quality_1,
        "quality_2": quality_2,
        "quality_3": quality_3,
        "robid":robid,
        "data_id": data_id,
        "date": date,
        "time": Time,
    })
    
    mqttc.publish(TOPIC, str(message))
    print("Published ")
    print(serial_number, robid, temperature, latitude,longitude, quality_1, quality_2, quality_3, data_id, date, Time)
    time.sleep(1)