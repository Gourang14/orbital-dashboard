
# # Generate random values and insert into the table
# for _ in range(2):  # Generate 2 random records
#     serial_number = random.randint(1, 100)
#     data_id = 'data_' + str(random.randint(1, 100))
#     robot_id = 'robot_' + str(random.randint(1, 100))
#     topic = 'topic_' + str(random.randint(1, 100))
#     temperature = round(random.uniform(-20, 50), 2)
#     latitude = round(random.uniform(-90, 90), 6)
#     longitude = round(random.uniform(-180, 180), 6)

#     insert_query = "INSERT INTO gps_data (serial_number, data_id, robot_id, topic, temperature, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#     insert_values = (serial_number, data_id, robot_id, topic, temperature, latitude, longitude)
#     mysql_cursor.execute(insert_query, insert_values)

# mysql_connection.commit()
# mysql_cursor.close()
# mysql_connection.close()

import random
import mysql.connector
from datetime import datetime

# MySQL configuration
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Agarwal54321'
MYSQL_DB = 'gps_data'

# Establish MySQL connection
try:
    mysql_connection = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
    mysql_cursor = mysql_connection.cursor()

    # Generate and insert random data into the table
    for _ in range(2):  # Generate 2 random records
        serial_number = random.randint(1, 100)
        robot_id = 'robot_' + str(random.randint(1, 100))
        topic = 'topic_' + str(random.randint(1, 100))
        temperature = round(random.uniform(-20, 50), 2)
        latitude = round(random.uniform(-90, 90), 6)
        longitude = round(random.uniform(-180, 180), 6)
        quality_1 = round(random.uniform(1, 100), 2)
        quality_2 = round(random.uniform(1, 100), 2)
        quality_3 = round(random.uniform(1, 100), 2)
        data_id = 'data_' + str(random.randint(1, 100))
        current_datetime = datetime.now()

        # Extract date and time components
        date = current_datetime.date()
        time = current_datetime.time()

        insert_query = "INSERT INTO gps_data (serial_number, robot_id, topic, temperature, latitude, longitude, quality_1, quality_2, quality_3, data_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_values = (serial_number, robot_id, topic, temperature, latitude, longitude, quality_1, quality_2, quality_3, data_id)
        mysql_cursor.execute(insert_query, insert_values)

    mysql_connection.commit()
    print("Data insertion successful.")

except mysql.connector.Error as e:
    print("Error connecting to MySQL:", e)

finally:
    if 'mysql_connection' in locals() or 'mysql_connection' in globals():
        mysql_cursor.close()
        mysql_connection.close()

