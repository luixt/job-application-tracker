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

def get_company_by_id(company_id):
    """Fetches a single company for the Edit form."""
    query = "SELECT * FROM companies WHERE company_id = %s"
    result = execute_query(query, (company_id,), fetch=True)
    return result[0] if result else None

def update_company(company_id, data):
    query = """
        UPDATE companies 
        SET company_name=%s, industry=%s, website=%s, city=%s, state=%s, notes=%s
        WHERE company_id=%s
    """
    params = (
        data['name'], data['industry'], data['website'], 
        data['city'], data['state'], data['notes'], company_id
    )
    return execute_query(query, params)

def delete_company(company_id):
    return execute_query("DELETE FROM companies WHERE company_id = %s", (company_id,))

# JOBS DATA LOGIC
def get_all_jobs():
    """Fetches all jobs joined with their company names."""
    query = """
        SELECT j.*, c.company_name 
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY j.date_posted DESC
    """
    return execute_query(query, fetch=True)

def create_job(data):
    """Inserts a new job. Note: requirements is passed as a JSON string."""
    query = """
        INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        data['company_id'], data['title'], data['type'],
        data['s_min'], data['s_max'], data['url'], 
        data['date'], data['reqs'] # reqs should be a JSON string
    )
    return execute_query(query, params)

def get_job_by_id(job_id):
    """Fetches a single job record."""
    query = "SELECT * FROM jobs WHERE job_id = %s"
    result = execute_query(query, (job_id,), fetch=True)
    return result[0] if result else None

def update_job(job_id, data):
    """Updates an existing job record."""
    query = """
        UPDATE jobs 
        SET company_id=%s, job_title=%s, job_type=%s, salary_min=%s, 
            salary_max=%s, job_url=%s, date_posted=%s, requirements=%s
        WHERE job_id=%s
    """
    params = (
        data['company_id'], data['title'], data['type'], data['s_min'],
        data['s_max'], data['url'], data['date'], data['reqs'], job_id
    )
    return execute_query(query, params)

def delete_job(job_id):
    return execute_query("DELETE FROM jobs WHERE job_id = %s", (job_id,))

# APPLICATIONS DATA LOGIC
def get_all_applications():
    """Fetches applications with detailed Job and Company info."""
    query = """
        SELECT a.*, j.job_title, j.job_url, c.company_name 
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC
    """
    return execute_query(query, fetch=True)

def get_application_by_id(app_id):
    return execute_query("SELECT * FROM applications WHERE application_id = %s", (app_id,), fetch=True)[0]

def create_application(data):
    query = """
        INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (data['job_id'], data['date'], data['status'], data['resume'], data['cv_sent'], data['interview_json'])
    return execute_query(query, params)

def update_application(app_id, data):
    query = """
        UPDATE applications 
        SET job_id=%s, application_date=%s, status=%s, resume_version=%s, cover_letter_sent=%s
        WHERE application_id=%s
    """
    params = (data['job_id'], data['date'], data['status'], data['resume'], data['cv_sent'], app_id)
    return execute_query(query, params)

def delete_application(app_id):
    return execute_query("DELETE FROM applications WHERE application_id = %s", (app_id,))

# CONTACTS DATA LOGIC
def get_all_contacts():
    """Fetches all contacts joined with their company names."""
    query = """
        SELECT c.*, comp.company_name 
        FROM contacts c
        JOIN companies comp ON c.company_id = comp.company_id
        ORDER BY c.contact_name ASC
    """
    return execute_query(query, fetch=True)

def get_contact_by_id(contact_id):
    return execute_query("SELECT * FROM contacts WHERE contact_id = %s", (contact_id,), fetch=True)[0]

def create_contact(data):
    query = """
        INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (data['company_id'], data['name'], data['title'], data['email'], data['phone'], data['linkedin'], data['notes'])
    return execute_query(query, params)

def update_contact(contact_id, data):
    query = """
        UPDATE contacts 
        SET company_id=%s, contact_name=%s, title=%s, email=%s, phone=%s, linkedin_url=%s, notes=%s
        WHERE contact_id=%s
    """
    params = (data['company_id'], data['name'], data['title'], data['email'], data['phone'], data['linkedin'], data['notes'], contact_id)
    return execute_query(query, params)

def delete_contact(contact_id):
    return execute_query("DELETE FROM contacts WHERE contact_id = %s", (contact_id,))