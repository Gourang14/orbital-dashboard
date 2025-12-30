# import pandas as pd
# import datetime
# import matplotlib.pyplot as plt
# from matplotlib import style
# style.use('ggplot')

# # # read data and create a df, it will take all page tables

# import mysql.connector

# try:
#     connection = mysql.connector.connect(host='localhost',
#                                          database='gps_data',
#                                          user='root',
#                                          password='Agarwal@54321')
#     sql_query = pd.read_sql('SELECT * FROM gps_data', connection)
#     print(connection)
#     df = pd.DataFrame(sql_query, columns = [ 'id', 'robot_id','temperature', 'latitude', 'longitude', 'quality_1', 'quality_2', 'quality_3', 'data_id'])
    
#     # sql_select_Query = "select * from gps_data"
#     # cursor = connection.cursor()
#     # cursor.execute(sql_select_Query)
#     # get all records
    
#     # df = pd.read_sql_table
#     # df = df[0]
#     # df.set_index(df.columns[0],).plot(figsize=(15,8))
#     # print(df)
    

# # Save the plots as PNG images
#     df.plot(df.columns[0], df.columns[2], figsize=(18, 8))
#     plt.savefig('./webpage/temperature.png')

#     df.plot(df.columns[0], df.columns[3], figsize=(18, 8)) 
#     plt.savefig('./webpage/latitude.png')

#     df.plot(df.columns[0], df.columns[4], figsize=(18, 8))
#     plt.savefig('./webpage/longitude.png')

#     # Close the plots
#     plt.close('all')
#     # plt.show()
    

# except mysql.connector.Error as e:
#     print("Error reading data from MySQL table", e)

# import pandas as pd
# import matplotlib.pyplot as plt
# from sqlalchemy import create_engine
# import os

# # Database connection parameters
# MYSQL_HOST = 'localhost'
# MYSQL_DB = 'gps_data'
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = 'Agarwal54321'

# # Output directory for plots
# output_dir = './webpage'

# # Ensure the output directory exists
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# try:
#     # Create SQLAlchemy engine with the correct connection string format
#     engine = create_engine(f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}')

#     # Read data from MySQL into a Pandas DataFrame
#     df = pd.read_sql('SELECT * FROM gps_data', con=engine)
#     print("Data loaded successfully from MySQL.")

#     # Plotting examples (replace with your specific plotting logic)
#     df.plot(df.columns[0], df.columns[2], figsize=(18, 8))
#     plt.savefig('./webpage/temperature.png')

#     df.plot(df.columns[0], df.columns[3], figsize=(18, 8)) 
#     plt.savefig('./webpage/latitude.png')

#     df.plot(df.columns[0], df.columns[4], figsize=(18, 8))
#     plt.savefig('./webpage/longitude.png')

#     plt.close('all')

# except Exception as e:
#     print("Error:", e)


# import pandas as pd
# import matplotlib.pyplot as plt
# from sqlalchemy import create_engine
# import os

# # Database connection parameters
# MYSQL_HOST = 'localhost'
# MYSQL_DB = 'gps_data'
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = 'Agarwal54321'

# # Output directory for plots
# output_dir = './webpage'

# # Ensure the output directory exists
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# try:
#     # Create SQLAlchemy engine with the correct connection string format
#     engine = create_engine(f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}')

#     # Read data from MySQL into a Pandas DataFrame
#     df = pd.read_sql('SELECT * FROM gps_data', con=engine)
#     print("Data loaded successfully from MySQL.")

#     # Plotting examples (replace with your specific plotting logic)
#     if 'temperature' in df.columns and 'latitude' in df.columns and 'longitude' in df.columns:
#         # Plot temperature
#         df.plot(x=df.columns[0], y='temperature', figsize=(18, 8))
#         plt.title('Temperature')
#         plt.xlabel('Index')
#         plt.ylabel('Temperature')
#         plt.savefig(os.path.join(output_dir, 'temperature.png'))
#         plt.close()

#         # Plot latitude
#         df.plot(x=df.columns[0], y='latitude', figsize=(18, 8))
#         plt.title('Latitude')
#         plt.xlabel('Index')
#         plt.ylabel('Latitude')
#         plt.savefig(os.path.join(output_dir, 'latitude.png'))
#         plt.close()

#         # Plot longitude
#         df.plot(x=df.columns[0], y='longitude', figsize=(18, 8))
#         plt.title('Longitude')
#         plt.xlabel('Index')
#         plt.ylabel('Longitude')
#         plt.savefig(os.path.join(output_dir, 'longitude.png'))
#         plt.close()

#     else:
#         print("Error: Required columns not found in the dataset.")

# except Exception as e:
#     print("Error:", e)

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os
from sqlalchemy import create_engine

# Database connection parameters
MYSQL_HOST = 'localhost'
MYSQL_DB = 'gps_data'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Agarwal54321'

# Output directory for plots
output_dir = './webpage'

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

try:
    # Create SQLAlchemy engine with the correct connection string format
    engine = create_engine(f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}')

    # Read data from MySQL into a Pandas DataFrame
    df = pd.read_sql('SELECT * FROM gps_data', con=engine)
    print("Data loaded successfully from MySQL.")

    # Check if required columns exist in the DataFrame
    if 'temperature' in df.columns and 'robot_id' in df.columns and 'quality_1' in df.columns and 'quality_2' in df.columns and 'quality_3' in df.columns:
        # Plot bar chart for average temperature
        robot_ids = df['robot_id'].unique()
        avg_temperatures = [df[df['robot_id'] == rid]['temperature'].mean() for rid in robot_ids]

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.bar(robot_ids, avg_temperatures, color='skyblue')
        ax.set_xlabel('Robot ID')
        ax.set_ylabel('Average Temperature')
        ax.set_title('Average Temperature per Robot')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'average_temperature_per_robot.png'))
        plt.close()
        print("Average temperature bar chart saved successfully.")

        # Calculate mean of quality columns
        quality_means = {
            'Quality 1': df['quality_1'].mean(),
            'Quality 2': df['quality_2'].mean(),
            'Quality 3': df['quality_3'].mean()
        }

        # Create Pie Chart using Plotly
        labels = list(quality_means.keys())
        values = list(quality_means.values())

        fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig.update_layout(
            title='Quality Distribution',
            template='plotly_white',
            height=600,
            width=800
        )

        plot_img = os.path.join(output_dir, 'quality_distribution.png')
        fig.write_image(plot_img)
        print("Quality distribution pie chart saved successfully.")

    else:
        print("Error: Required columns not found in the dataset.")

except Exception as e:
    print("Error:", e)














