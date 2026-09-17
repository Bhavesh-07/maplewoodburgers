import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.environ.get('DB_HOST', '127.0.0.1'),
        port=int(os.environ.get('DB_PORT', 3306)),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASS', ''),
        database=os.environ.get('DB_NAME', 'maplewood_db')
    )
    print("MySQL Connection Success to database:", os.environ.get('DB_NAME', 'maplewood_db'))
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    print("Existing tables:", tables)
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
