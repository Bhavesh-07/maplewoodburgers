import mysql.connector
try:
    conn = mysql.connector.connect(host='127.0.0.1', user='root', password='')
    print("MySQL Connection Success")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
