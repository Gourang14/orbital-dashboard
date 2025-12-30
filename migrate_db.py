import pymysql
import sqlite3
import datetime

# MySQL configuration (from app.py)
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Agarwal54321'
MYSQL_DB = 'gps_data'

def get_mysql_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def map_type(mysql_type):
    mysql_type = mysql_type.upper()
    if 'INT' in mysql_type: return 'INTEGER'
    if 'FLOAT' in mysql_type or 'DOUBLE' in mysql_type or 'DECIMAL' in mysql_type: return 'REAL'
    return 'TEXT'

def migrate():
    print("Connecting to MySQL...")
    try:
        mysql_conn = get_mysql_connection()
    except Exception as e:
        print(f"Failed to connect to MySQL: {e}")
        return

    print("Connecting to SQLite...")
    sqlite_conn = sqlite3.connect('gps_data.db')
    sqlite_cursor = sqlite_conn.cursor()

    try:
        with mysql_conn.cursor() as cursor:
            # Get table schema
            table_name = 'gps_data'
            print(f"Fetching schema for table: {table_name}")
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            
            create_query_parts = []
            column_names = []
            
            for col in columns:
                col_name = col['Field']
                col_type = col['Type']
                sqlite_type = map_type(col_type)
                create_query_parts.append(f"{col_name} {sqlite_type}")
                column_names.append(col_name)
            
            create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(create_query_parts)});"
            print(f"Creating SQLITE table: {create_query}")
            sqlite_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            sqlite_cursor.execute(create_query)
            
            # Fetch Data
            print("Fetching data from MySQL...")
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            print(f"Migrating {len(rows)} rows...")
            insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(['?']*len(column_names))})"
            
            sqlite_rows = []
            for row in rows:
                values = []
                for col in column_names:
                    val = row[col]
                    if isinstance(val, (datetime.date, datetime.datetime)):
                        val = val.isoformat()
                    elif isinstance(val, datetime.timedelta):
                        val = str(val) # Convert timedelta to string "H:M:S"
                    values.append(val)
                sqlite_rows.append(tuple(values))
                
            sqlite_cursor.executemany(insert_query, sqlite_rows)
            sqlite_conn.commit()
            print("Migration successful!")
            
    finally:
        mysql_conn.close()
        sqlite_conn.close()

if __name__ == "__main__":
    migrate()
