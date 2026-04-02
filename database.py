import mysql.connector
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# DATABASE CONNECTION AND QUERY FUNCTIONS
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

    
# DASHBOARD DATA LOGIC
def get_dashboard_stats():
    """Fetches counts for companies, jobs, and applications."""
    comp_count = execute_query("SELECT COUNT(*) as count FROM companies", fetch=True)[0]['count']
    job_count = execute_query("SELECT COUNT(*) as count FROM jobs", fetch=True)[0]['count']
    app_count = execute_query("SELECT COUNT(*) as count FROM applications", fetch=True)[0]['count']
    return {
        'companies': comp_count,
        'jobs': job_count,
        'applications': app_count
    }

def get_recent_applications(limit=5):
    """Fetches the most recent job applications with joined company names."""
    query = """
        SELECT a.application_date, j.job_title, c.company_name, a.status 
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC LIMIT %s
    """
    return execute_query(query, (limit,), fetch=True)

# COMPANIES DATA LOGIC
def get_all_companies():
    return execute_query("SELECT * FROM companies ORDER BY company_name ASC", fetch=True)

def create_company(data):
    query = """
        INSERT INTO companies (company_name, industry, website, city, state, notes)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        data['name'], data['industry'], data['website'], 
        data['city'], data['state'], data['notes']
    )
    return execute_query(query, params)

def delete_company(company_id):
    return execute_query("DELETE FROM companies WHERE company_id = %s", (company_id,))

