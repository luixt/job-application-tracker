import mysql.connector
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database.
    """
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def execute_query(query, params=None, fetch=False):
    """
    A helper function to run queries and handle connection closing.
    - query: The SQL string
    - params: Tuple of values for placeholders (%)
    - fetch: True if you expect results back (SELECT)
    """
    conn = get_db_connection()
    if conn is None:
        return None
    
    cursor = conn.cursor(dictionary=True) # Returns results as dictionaries
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid
        return result
    finally:
        cursor.close()
        conn.close()