import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="system",
        database="e2e_chatapp"
    )

if __name__ == "__main__":
    try:
        conn = get_db_connection()
        print("MySQL connection successful")
        conn.close()
    except Exception as e:
        print("Error:", e)
