from flask import Flask, json, render_template, request, redirect, flash, url_for
# Import all our data functions from database.py
from database import (
    get_dashboard_stats, get_recent_applications, get_all_companies, 
    create_company, get_company_by_id, update_company, delete_company, 
    get_all_jobs, create_job, delete_job, get_job_by_id, update_job
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
    edit_id = request.args.get('edit') # Check if "?edit=[id]" is in the URL
    company_to_edit = None

    # If we are in "Edit Mode", fetch the specific company data
    if edit_id:
        company_to_edit = get_company_by_id(edit_id)

    if request.method == 'POST':
        # Collect form data
        company_data = {
            'name': request.form.get('company_name'),
            'industry': request.form.get('industry'),
            'website': request.form.get('website'),
            'city': request.form.get('city'),
            'state': request.form.get('state'),
            'notes': request.form.get('notes')
        }
        
        # Check if we are UPDATING (id exists in hidden field) or CREATING
        existing_id = request.form.get('company_id')
        
        if existing_id:
            update_company(existing_id, company_data)
            flash(f"Company '{company_data['name']}' updated!", "success")
        else:
            create_company(company_data)
            flash(f"Company '{company_data['name']}' added!", "success")
            
        return redirect(url_for('companies'))

    # Always fetch the full list for the table
    companies_list = get_all_companies()
    return render_template('companies.html', 
                           companies=companies_list, 
                           edit_mode=company_to_edit)

# Companies Delete Route
@app.route('/companies/delete/<int:id>')
def delete_company_route(id):
    delete_company(id)
    flash("Company deleted successfully!", "danger")
    return redirect(url_for('companies'))

# Companies Edit Route
@app.route('/companies/edit/<int:id>', methods=['GET', 'POST'])
def edit_company(id):
    company = get_company_by_id(id)
    
    if request.method == 'POST':
        company_data = {
            'name': request.form.get('company_name'),
            'industry': request.form.get('industry'),
            'website': request.form.get('website'),
            'city': request.form.get('city'),
            'state': request.form.get('state'),
            'notes': request.form.get('notes')
        }
        update_company(id, company_data)
        flash(f"Company '{company_data['name']}' updated!", "success")
        return redirect(url_for('companies'))
    
    return render_template('edit_company.html', company=company)

# --- JOBS ---
# Combined Create/Edit route for Jobs to simplify form handling
@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    edit_id = request.args.get('edit')
    job_to_edit = None

    if edit_id:
        job_to_edit = get_job_by_id(edit_id)
        # Convert JSON requirements back to a string for the form input
        if job_to_edit and job_to_edit['requirements']:
            job_to_edit['reqs_str'] = ", ".join(json.loads(job_to_edit['requirements']))

    if request.method == 'POST':
        skills_list = [s.strip() for s in request.form.get('requirements').split(',') if s.strip()]
        
        job_data = {
            'company_id': request.form.get('company_id'),
            'title': request.form.get('job_title'),
            'type': request.form.get('job_type'),
            's_min': request.form.get('salary_min') or None,
            's_max': request.form.get('salary_max') or None,
            'url': request.form.get('job_url'),
            'date': request.form.get('date_posted'),
            'reqs': json.dumps(skills_list)
        }
        
        job_id = request.form.get('job_id')
        if job_id:
            update_job(job_id, job_data)
            flash("Job updated successfully!", "success")
        else:
            create_job(job_data)
            flash("Job posted successfully!", "success")
            
        return redirect(url_for('jobs'))

    return render_template('jobs.html', 
                           jobs=get_all_jobs(), 
                           companies=get_all_companies(), 
                           edit_mode=job_to_edit)

# Jobs Delete Route
@app.route('/jobs/delete/<int:id>')
def delete_job_route(id):
    delete_job(id)
    flash("Job deleted.", "danger")
    return redirect(url_for('jobs'))

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