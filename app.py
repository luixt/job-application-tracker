from flask import Flask, render_template, request, redirect, flash, url_for
from database import execute_query

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def dashboard():
    comp_count = execute_query("SELECT COUNT(*) as count FROM companies", fetch=True)[0]['count']
    job_count = execute_query("SELECT COUNT(*) as count FROM jobs", fetch=True)[0]['count']
    app_count = execute_query("SELECT COUNT(*) as count FROM applications", fetch=True)[0]['count']
    
    recent_apps = execute_query("""
        SELECT a.application_date, j.job_title, c.company_name, a.status 
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC LIMIT 5
    """, fetch=True)

    stats = {
        'companies': comp_count,
        'jobs': job_count,
        'applications': app_count
    }
    
    return render_template('dashboard.html', stats=stats, recent_apps=recent_apps)

@app.route('/companies')
def companies():
    return render_template('companies.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/applications')
def applications():
    return render_template('applications.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/match')
def job_match():
    return render_template('job_match.html')

if __name__ == '__main__':
    app.run(debug=True)