from flask import Flask, render_template, request, redirect, flash, url_for
# Import all our data functions from database.py
from database import (
    get_dashboard_stats, 
    get_recent_applications, 
    get_all_companies, 
    create_company
)

app = Flask(__name__)
app.secret_key = 'supersecretkey' # Required for session-based flash messages

# --- DASHBOARD ---
@app.route('/')
def dashboard():
    stats = get_dashboard_stats()
    recent_apps = get_recent_applications()
    return render_template('dashboard.html', stats=stats, recent_apps=recent_apps)

# --- COMPANIES ---
@app.route('/companies', methods=['GET', 'POST'])
def companies():
    if request.method == 'POST':
        company_data = {
            'name': request.form.get('company_name'),
            'industry': request.form.get('industry'),
            'website': request.form.get('website'),
            'city': request.form.get('city'),
            'state': request.form.get('state'),
            'notes': request.form.get('notes')
        }
        create_company(company_data)
        flash(f"Company '{company_data['name']}' added!", "success")
        return redirect(url_for('companies'))

    companies_list = get_all_companies()
    return render_template('companies.html', companies=companies_list)

# --- PLACEHOLDERS FOR NEXT STEPS ---
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