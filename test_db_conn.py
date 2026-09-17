import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASS', ''),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
}

try:
    conn = mysql.connector.connect(**config)
    print("Connection successful!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")
