# import multiprocessing
# import subprocess
# from flask import Flask, render_template, jsonify, request
# from pymongo import MongoClient
# from pymongo import TEXT
# from statistics import mean, median, mode
# import mysql.connector
# import matplotlib.pyplot as plt
# import csv
# import pandas as pd
# import matplotlib.pyplot as plt
# import io
# import base64
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from plotly.subplots import make_subplots
# import numpy as np
# import plotly.graph_objects as go
# from flask import render_template_string
# from flask import Flask, render_template
# # import mysql.connector
# # import matplotlib.pyplot as plt
# from matplotlib.patches import Patch
# import mpld3
# import pymysql
# from scipy import stats

# app = Flask(__name__, static_folder='static')

# # # MongoDB configuration
# # MONGO_HOST = 'mongodb+srv://pa:prashant@cluster0.5b0djvj.mongodb.net/'
# # MONGO_PORT = 27017
# # MONGO_DB = 'gps_data'
# # COLLECTION_NAME = 'gps_messages'
# # USERNAME = 'pa'
# # PASSWORD = 'prashant'

# # Mysql
# MYSQL_HOST = 'localhost'
# MYSQL_PORT = 3306
# MYSQL_DB = 'gps_data'
# MYSQL_USER = 'root'
# MYSQL_PASSWORD = 'Agarwal54321'

# quality_cutoffs = {
#     'quality_1': 20,
#     'quality_2': 30,
#     'quality_3': 50
# }

# def get_data_from_db():
#     connection = pymysql.connect(
#         host='localhost',
#         user='root',
#         password='Agarwal54321',
#         db='gps_data',
#         charset='utf8mb4',
#         cursorclass=pymysql.cursors.DictCursor
#     )

#     try:
#         with connection.cursor() as cursor:
#             sql = "SELECT temperature, quality_1, quality_2, quality_3 FROM gps_messages"
#             cursor.execute(sql)
#             result = cursor.fetchall()
#     finally:
#         connection.close()
#     return result

# def calculate_statistics(data, key):
#     values = [entry[key] for entry in data if entry[key] is not None]
#     mean = np.mean(values)
#     median = np.median(values)
#     mode = stats.mode(values)[0][0]
#     return mean, median, mode

# @app.route('/delete', methods=['DELETE'])
# def delete_data():
#     try:
#         mysql_connection = mysql.connector.connect(
#             host=MYSQL_HOST,
#             port=MYSQL_PORT,
#             user=MYSQL_USER,
#             password=MYSQL_PASSWORD,
#             database=MYSQL_DB
#         )
#         mysql_cursor = mysql_connection.cursor()
#         mysql_cursor.execute("DELETE FROM gps_data")
#         mysql_cursor.execute("ALTER TABLE gps_data AUTO_INCREMENT = 1")
#         mysql_connection.commit()
#         mysql_cursor.close()
#         mysql_connection.close()

#         if mysql_cursor.rowcount > 0:
#             print("Data deleted from MySQL")
#         else:
#             print("No data deleted from MySQL")

#         deleted_count = 100
#         return jsonify({'message': 'Data deleted successfully', 'deleted_count': deleted_count}), 200
#     except Exception as e:
#         return jsonify({'message': 'Failed to delete data', 'error': str(e)}), 500


# @app.route('/')
# @app.route('/<robot_ids>')

# def display_data_route(robot_ids=None):
#     mysql_connection = mysql.connector.connect(
#         host=MYSQL_HOST,
#         port=MYSQL_PORT,
#         user=MYSQL_USER,
#         password=MYSQL_PASSWORD,
#         database=MYSQL_DB
#     )
#     mysql_cursor = mysql_connection.cursor()
#     if robot_ids:
#         robot_id_list = robot_ids.split(',')

#         query = "SELECT * FROM gps_data WHERE robot_id IN (%s)" % (
#             ','.join(['%s'] * len(robot_id_list)))

#         mysql_cursor.execute(query, tuple(robot_id_list))

#         columns = [column[0] for column in mysql_cursor.description]
#         data = [dict(zip(columns, row)) for row in mysql_cursor.fetchall()]
#     else:
#         mysql_cursor.execute("SELECT * FROM gps_data")
#         columns = [column[0] for column in mysql_cursor.description]
#         data = [dict(zip(columns, row)) for row in mysql_cursor.fetchall()]

#     return render_template('./index.html', data=data)


# def run_subscriber():
#     subprocess.run(['python', './subscribe.py'])


# def generate_plot(data):
#     fig = go.Figure()

#     fig.add_trace(go.Scatter(
#         x=data.iloc[:, 0], y=data.iloc[:, 7], name='Quality 1'))

#     fig.add_trace(go.Scatter(
#         x=data.iloc[:, 0], y=data.iloc[:, 8], name='Quality 2'))

#     fig.add_trace(go.Scatter(
#         x=data.iloc[:, 0], y=data.iloc[:, 9], name='Quality 3'))

#     fig.add_trace(go.Scatter(
#         x=data.iloc[:, 0], y=data.iloc[:, 4], name='Temperature'))

#     fig.update_layout(
#         title='Sensor Data vs Time',
#         xaxis_title='Time',
#         yaxis_title='Values in SI Unit',
#         hovermode='closest',
#         template='plotly_white',
#         height=600,
#         width=1150,
#         paper_bgcolor='rgb(22, 40, 88)',
#         plot_bgcolor='rgb(22, 40, 88)',
#         font_family="Courier New",
#         font_color="rgb(138, 228, 255)",
#         title_font_family="Times New Roman",
#         title_font_color="rgb(138, 228, 255)",
#         font_size=20,
#     )

#     plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

#     return plot_html


# @app.route('/data')
# def get_data():
#     connection = mysql.connector.connect(
#         host=MYSQL_HOST,
#         port=MYSQL_PORT,
#         database=MYSQL_DB,
#         user=MYSQL_USER,
#         password=MYSQL_PASSWORD
#     )

#     query = "SELECT * FROM gps_data ORDER BY id DESC LIMIT 50"
#     data = pd.read_sql(query, connection)

#     connection.close()

#     data_json = data.to_json(orient='records')
#     return data_json

# @app.route('/indexgr')
# def indexgr():
#     return render_template('indexgr.html')

# @app.route('/graphs')
# def index():
#     connection = mysql.connector.connect(
#         host=MYSQL_HOST,
#         port=MYSQL_PORT,
#         database=MYSQL_DB,
#         user=MYSQL_USER,
#         password=MYSQL_PASSWORD
#     )
#     cursor = connection.cursor()
#     query = "SELECT id AS data_id, DATE(timestamp) AS date, TIME(timestamp) AS time, robot_id, AVG(temperature) AS average_temperature FROM gps_data GROUP BY robot_id, date, time UNION SELECT 'Global Avg' AS robot_id, NULL AS date, NULL AS time, AVG(temperature) AS average_temperature FROM gps_data  order by robot_id ASC "
#     cursor.execute(query)
#     temperature_results = cursor.fetchall()

#     query = "SELECT id AS data_id, DATE(timestamp) AS date, TIME(timestamp) AS time, robot_id, AVG(quality_1) AS average_quality_1 FROM gps_data GROUP BY robot_id, date, time UNION SELECT 'Global Avg' AS robot_id, NULL AS date, NULL AS time, AVG(quality_1) AS average_quality_1 FROM gps_data order by robot_id ASC"
#     cursor.execute(query)
#     quality_1_results = cursor.fetchall()

#     query = "SELECT id AS data_id, DATE(timestamp) AS date, TIME(timestamp) AS time, robot_id, AVG(quality_2) AS average_quality_2 FROM gps_data GROUP BY robot_id, date, time UNION SELECT 'Global Avg' AS robot_id, NULL AS date, NULL AS time, AVG(quality_2) AS average_quality_2 FROM gps_data order by robot_id ASC"
#     cursor.execute(query)
#     quality_2_results = cursor.fetchall()

#     query = "SELECT id AS data_id, DATE(timestamp) AS date, TIME(timestamp) AS time, robot_id, AVG(quality_3) AS average_quality_3 FROM gps_data GROUP BY robot_id, date, time UNION SELECT 'Global Avg' AS robot_id, NULL AS date, NULL AS time, AVG(quality_3) AS average_quality_3 FROM gps_data order by robot_id ASC"
#     cursor.execute(query)
#     quality_3_results = cursor.fetchall()

#     temperature_x = []
#     temperature_y = []
#     for row in temperature_results:
#         temperature_x.append(row[0])
#         temperature_y.append(row[1])

#     quality_1_x = []
#     quality_1_y = []
#     for row in quality_1_results:
#         quality_1_x.append(row[0])
#         quality_1_y.append(row[1])

#     quality_2_x = []
#     quality_2_y = []
#     for row in quality_2_results:
#         quality_2_x.append(row[0])
#         quality_2_y.append(row[1])

#     quality_3_x = []
#     quality_3_y = []
#     for row in quality_3_results:
#         quality_3_x.append(row[0])
#         quality_3_y.append(row[1])
#     # bfig = go.Figure()

#     # bfig.add_trace(go.Bar(x=temperature_x, y=temperature_y, name='Average Temperature'))
#     # bfig.add_trace(go.Bar(x=quality_1_x, y=quality_1_y, name='Average Quality 1'))
#     # bfig.add_trace(go.Bar(x=quality_2_x, y=quality_2_y, name='Average Quality 2'))
#     # bfig.add_trace(go.Bar(x=quality_3_x, y=quality_3_y, name='Average Quality 3'))

#     # bfig.update_layout(
#     #     barmode='group',
#     #     xaxis_title='Robot IDs',
#     #     yaxis_title='Average Value',
#     #     title='Average Values for Temperature and Quality Metrics'
#     # )

#     # bgraph_data = bfig.to_html(full_html=False)
#     bfig = make_subplots(rows=3, cols=1, subplot_titles=[
#         # 'Average Temperature',
#         'Average Quality 1',
#         'Average Quality 2',
#         'Average Quality 3'
#     ])

#     # bfig.add_trace(go.Bar(x=temperature_x, y=temperature_y, name='Average Temperature'), row=1, col=1)
#     bfig.add_trace(go.Bar(x=quality_1_x, y=quality_1_y,
#                    name='Average Quality 1'), row=1, col=1)
#     bfig.add_trace(go.Bar(x=quality_2_x, y=quality_2_y,
#                    name='Average Quality 2'), row=2, col=1)
#     bfig.add_trace(go.Bar(x=quality_3_x, y=quality_3_y,
#                    name='Average Quality 3'), row=3, col=1)

#     bfig.update_layout(
#         height=950,
#         width=635,
#         title_text='Average Values for Quality Metrics',
#         showlegend=False,
#         paper_bgcolor='rgb(22, 40, 88)',
#         plot_bgcolor='rgb(22, 40, 88)',
#         font_family="Courier New",
#         font_size=20,

#         font_color="rgb(138, 228, 255)",
#         title_font_family="Times New Roman",
#         title_font_color="rgb(138, 228, 255)",
#         # title_font_size=20,
#         title={

#             'font': {'size': 20}
#         }
#         # legend_title_font_color="rgb(138, 228, 255)",
#         # legend_title_font_size=20,
#     )
#     bargraph_data = bfig.to_html(full_html=False)
#     # Close the database connection
#     # connection.close()

#     # _________________________________________________________________________________________

#     fig, axs = plt.subplots(1, 3, figsize=(17, 6), subplot_kw={'aspect': 'equal'})

#     for i, quality in enumerate(quality_cutoffs.keys()):
#         ax = axs[i]
#         ax.set_title(quality.capitalize(), fontsize=20, color= '#8ae4ff', fontweight='bold')

#         cursor.execute(f"SELECT robot_id, {quality} FROM gps_data ORDER BY robot_id ASC")
#         rows = cursor.fetchall()

#         filtered_values = [row for row in rows if row[1] > quality_cutoffs[quality]]

#         unique_robot_ids = list(set(row[0] for row in filtered_values))
#         robot_counts = [sum(1 for row in filtered_values if row[0] == robot_id) for robot_id in unique_robot_ids]

#         num_robot_ids = len(unique_robot_ids)
#         radii = [0.3 + i * 0.2 for i in range(num_robot_ids)]  # Increase the radius values for larger circles
#         labels = unique_robot_ids

#         legend_labels = []
#         legend_handles = []
#         legend_notations = []

#         colors = plt.cm.get_cmap('tab20')(range(num_robot_ids))

#         wedge_width = 1 / num_robot_ids

#         for radius, label, count, color in zip(radii, labels, robot_counts, colors):
#             if count > 0:
#                 percentage = (count / len(filtered_values)) * 100
#                 notation = f"{percentage:.1f}%"
#                 wedgeprops = {'width': wedge_width, 'edgecolor': 'w'}
#                 wedges, _ = ax.pie([count, len(filtered_values) - count], labels=['', ''],
#                                     radius=radius, colors=[color, 'lightgray'],
#                                     wedgeprops=wedgeprops)
#                 legend_labels.append(label)
#                 legend_handles.append(Patch(facecolor=color, edgecolor='w'))
#                 legend_notations.append(notation)

#         # Create the legend for the current subplot
#         legend = ax.legend(legend_handles, [f"{label} ({notation})" for label, notation in
#                                             zip(legend_labels, legend_notations)],
#                             loc='upper right', bbox_to_anchor=(0.69, 0), facecolor = '#162858', labelcolor='#8ae4ff')

#         # Add the legend to the subplot
#         ax.add_artist(legend)
#         ax.set_facecolor("#11224e")

#     plt.subplots_adjust(wspace=0.8)  # Adjust the spacing between subplots
#     html_string = mpld3.fig_to_html(fig)
#     # plt.savefig('static/temp_file5.png')  # Save the plot as a static file
#     # Create a buffer to store the plot image
#     # buffer = io.BytesIO()

#     # # Save the plot to the buffer
#     # plt.savefig(buffer, format='png')
#     # buffer.seek(0)

#     # # Convert the plot image to a base64-encoded string
#     # pie_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

# # Generate the HTML code to embed the plot



#     # _________________________________________________________________________________________

#     query = "SELECT * FROM gps_data ORDER BY id DESC LIMIT 50 "
#     data = pd.read_sql(query, connection)

#     plot_data = generate_plot(data)

#     connection.close()

#     num_values = int(request.args.get('num_values', 10))
#     last_values = data.tail(num_values)

#     quality_1_mean = round(mean(last_values['quality_1']), 2)
#     quality_1_median = round(median(last_values['quality_1']), 2)
#     quality_1_mode = round(mode(last_values['quality_1']), 2)
#     temperature_mean = round(mean(last_values['temperature']), 2)
#     temperature_median = round(median(last_values['temperature']), 2)
#     temperature_mode = round(mode(last_values['temperature']), 2)
#     quality_2_mean = round(mean(last_values['quality_2']), 2)
#     quality_2_median = round(median(last_values['quality_2']), 2)
#     quality_2_mode = round(mode(last_values['quality_2']), 2)
#     quality_3_mean = round(mean(last_values['quality_3']), 2)
#     quality_3_median = round(median(last_values['quality_3']), 2)
#     quality_3_mode = round(mode(last_values['quality_3']), 2)

#     return render_template('indexgr.html', plot_data=plot_data, quality_2_mode=quality_2_mode, quality_2_median=quality_2_median, quality_2_mean=quality_2_mean,
#                            temperature_mean=temperature_mean, temperature_median=temperature_median,
#                            temperature_mode=temperature_mode, quality_1_mode=quality_1_mode, quality_1_median=quality_1_median, quality_1_mean=quality_1_mean,
#                            quality_3_mode=quality_3_mode, quality_3_median=quality_3_median, quality_3_mean=quality_3_mean,
#                            bargraph_data=bargraph_data, html_string=html_string)


# if __name__ == '__main__':
#     subscriber_process = multiprocessing.Process(target=run_subscriber)
#     subscriber_process.start()
#     app.run()
#     subscriber_process.join()

from flask import Flask, render_template, jsonify, request
import mysql.connector
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from statistics import mean, median, mode
from scipy import stats
import subprocess
import multiprocessing
import sqlite3

app = Flask(__name__, static_folder='static')

DB_NAME = 'gps_data.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

quality_cutoffs = {
    'quality_1': 20,
    'quality_2': 30,
    'quality_3': 50
}

def get_data_from_db():
    connection = get_db_connection()

    try:
        cursor = connection.cursor()
        # Fetch all data for general display
        cursor.execute("SELECT * FROM gps_data")
        # Fetchall returns Row objects, convert to dicts if needed, or use as is
        # The frontend expects dict access (row['key']), which sqlite3.Row supports
        data = [dict(row) for row in cursor.fetchall()]

        # Fetch data for pie chart (distribution based on robot IDs)
        cursor.execute("SELECT robot_id, COUNT(*) AS count FROM gps_data GROUP BY robot_id")
        pie_chart_data = [dict(row) for row in cursor.fetchall()]

        # Fetch data for bar graph (average temperature across robots)
        bar_chart_data = []
        for quality in ['quality_1', 'quality_2', 'quality_3']:
            query = f"SELECT robot_id, AVG({quality}) AS avg_quality FROM gps_data GROUP BY robot_id"
            cursor.execute(query)
            result = [dict(row) for row in cursor.fetchall()]
            bar_chart_data.append(result)

    finally:
        connection.close()

    return data, pie_chart_data, bar_chart_data

def calculate_statistics(data, key):
    values = [entry[key] for entry in data if entry[key] is not None]
    if not values:
        return None, None, None

    mean_value = np.mean(values)
    median_value = np.median(values)

    # Calculate mode
    mode_result = stats.mode(values)
    mode_value = mode_result.mode[0] if isinstance(mode_result.mode, np.ndarray) and len(mode_result.mode) > 0 else mode_result.mode

    return mean_value, median_value, mode_value

@app.route('/delete', methods=['DELETE'])
def delete_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM gps_data")
        # Reset Auto Increment in SQLite
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='gps_data'")
        conn.commit()
        conn.close()

        print("Data deleted from SQLite")
        
        deleted_count = 100 # Mock count or fetch actual
        return jsonify({'message': 'Data deleted successfully', 'deleted_count': deleted_count}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to delete data', 'error': str(e)}), 500

@app.route('/')
@app.route('/<robot_ids>')
def display_data_route(robot_ids=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if robot_ids:
        robot_id_list = robot_ids.split(',')
        placeholders = ','.join(['?'] * len(robot_id_list))
        query = f"SELECT * FROM gps_data WHERE robot_id IN ({placeholders})"
        cursor.execute(query, robot_id_list)
        data = [dict(row) for row in cursor.fetchall()]
    else:
        cursor.execute("SELECT * FROM gps_data")
        data = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return render_template('./index.html', data=data)

def run_subscriber():
    subprocess.run(['python', './subscribe.py'])

def generate_plot(data):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data.iloc[:, 0], y=data.iloc[:, 7], name='Quality 1'))

    fig.add_trace(go.Scatter(
        x=data.iloc[:, 0], y=data.iloc[:, 8], name='Quality 2'))

    fig.add_trace(go.Scatter(
        x=data.iloc[:, 0], y=data.iloc[:, 9], name='Quality 3'))

    fig.add_trace(go.Scatter(
        x=data.iloc[:, 0], y=data.iloc[:, 4], name='Temperature'))

    fig.update_layout(
        title='Sensor Data vs Time',
        xaxis_title='Time',
        yaxis_title='Values in SI Unit',
        hovermode='closest',
        template='plotly_white',
        height=600,
        width=1150,
        paper_bgcolor='rgb(22, 40, 88)',
        plot_bgcolor='rgb(22, 40, 88)',
        font_family="Courier New",
        font_color="rgb(138, 228, 255)",
        title_font_family="Times New Roman",
        title_font_color="rgb(138, 228, 255)",
        font_size=20,
    )

    plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return plot_html

@app.route('/data')
def get_data():
    conn = get_db_connection()
    
    query = "SELECT * FROM gps_data ORDER BY id DESC LIMIT 50"
    data = pd.read_sql(query, conn)

    conn.close()

    data_json = data.to_json(orient='records')
    return data_json

@app.route('/indexgr')
def indexgr():
    data, pie_chart_data, bar_chart_data = get_data_from_db()

    temperature_mean, temperature_median, temperature_mode = calculate_statistics(data, 'temperature')
    quality_1_mean, quality_1_median, quality_1_mode = calculate_statistics(data, 'quality_1')
    quality_2_mean, quality_2_median, quality_2_mode = calculate_statistics(data, 'quality_2')
    quality_3_mean, quality_3_median, quality_3_mode = calculate_statistics(data, 'quality_3')

    # Call the graphs function with bar_chart_data
    bar_graph = graphs(bar_chart_data)
    pie_chart = generate_pie_chart(pie_chart_data)
    # Render the template with required data
    return render_template('indexgr.html',
                           temperature_mean=temperature_mean,
                           temperature_median=temperature_median,
                           temperature_mode=temperature_mode,
                           quality_1_mean=quality_1_mean,
                           quality_1_median=quality_1_median,
                           quality_1_mode=quality_1_mode,
                           quality_2_mean=quality_2_mean,
                           quality_2_median=quality_2_median,
                           quality_2_mode=quality_2_mode,
                           quality_3_mean=quality_3_mean,
                           quality_3_median=quality_3_median,
                           quality_3_mode=quality_3_mode,
                           bar_graph=bar_graph,
                           pie_chart=pie_chart)

@app.route('/graphs')
def graphs(bar_chart_data=None):
    if bar_chart_data is None:
        # Handle case where bar_chart_data is not provided or is invalid
        return "No data available", 500

    fig = make_subplots(rows=3, cols=1, subplot_titles=('Quality 1 vs Robot', 'Quality 2 vs Robot', 'Quality 3 vs Robot'))

    for i, quality_data in enumerate(bar_chart_data, start=1):
        quality = f'quality_{i}'  # quality_1, quality_2, quality_3
        color = 'green'
        color_d = 'orange'
        fig.add_trace(go.Bar(
            x=[d['robot_id'] for d in quality_data],
            y=[d['avg_quality'] for d in quality_data],
            name=quality,
            marker_color=[color if d['avg_quality'] >= quality_cutoffs[quality] else color_d for d in quality_data]
        ), row=i, col=1)

    fig.update_layout(showlegend=False, height=900)

    plot_html = fig.to_html(full_html=False)

    return plot_html

def generate_pie_chart(pie_chart_data):
    labels = [d['robot_id'] for d in pie_chart_data]
    values = [d['count'] for d in pie_chart_data]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(
        title='Data Distribution by Robot ID',
        template='plotly_white',
        height=400,
        width=600
    )

    pie_chart_html = fig.to_html(full_html=False)
    return pie_chart_html

@app.route('/map_data')
def get_map_data():
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        database=MYSQL_DB,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD
    )

    query = "SELECT latitude, longitude, robot_id, id AS data_id, temperature, quality_1, quality_2, quality_3 FROM gps_data"
    cursor = connection.cursor()
    cursor.execute(query)

    columns = [column[0] for column in cursor.description]
    map_data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    connection.close()

    return jsonify(map_data)

@app.route('/bar_chart_data')
def get_bar_chart_data():
    _, _, bar_data = get_data_from_db()
    return jsonify(bar_data)

@app.route('/pie_chart_data')
def get_pie_chart_data():
    _, pie_data, _ = get_data_from_db()
    return jsonify(pie_data)

@app.route('/space_dashboard')
def space_dashboard():
    return render_template('space_dashboard.html')

if __name__ == '__main__':
    subscriber_process = multiprocessing.Process(target=run_subscriber)
    subscriber_process.start()
    app.run(debug=True, use_reloader=False)
    subscriber_process.join()

