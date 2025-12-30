import mysql.connector
from datetime import datetime

# Database config
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DB = 'gps_data'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Agarwal54321'

def update_dates():
    try:
        conn = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        cursor = conn.cursor()
        
        # Update all rows to have the current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        print(f"Updating all records to date: {current_date}")
        
        query = "UPDATE gps_data SET date = %s"
        cursor.execute(query, (current_date,))
        conn.commit()
        
        print(f"Successfully updated {cursor.rowcount} records.")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    update_dates()
