from flask import Flask, json, render_template, request, redirect, flash, url_for
# Import all our data functions from database.py
from database import (
    get_dashboard_stats, get_recent_applications, get_all_companies, 
    create_company, get_company_by_id, update_company, delete_company, 
    get_all_jobs, create_job, delete_job, get_job_by_id, update_job,
    get_all_applications, get_application_by_id, create_application, 
    update_application, delete_application, get_all_contacts, get_contact_by_id, 
    create_contact, update_contact, delete_contact, get_all_jobs_for_matching
)

app = Flask(__name__)
app.secret_key = 'supersecretkey' # Required for session-based flash messages

@app.template_filter('from_json')
def from_json_filter(value):
    return json.loads(value) if value else []

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

# --- APPLICATIONS ---
@app.route('/applications', methods=['GET', 'POST'])
def applications():
    edit_id = request.args.get('edit')
    app_to_edit = None
    if edit_id:
        app_to_edit = get_application_by_id(edit_id)

    if request.method == 'POST':
        app_data = {
            'job_id': request.form.get('job_id'),
            'date': request.form.get('application_date'),
            'status': request.form.get('status'),
            'resume': request.form.get('resume_version'),
            'cv_sent': 1 if request.form.get('cover_letter_sent') else 0,
            'interview_json': json.dumps({}) # Placeholder for future feature
        }
        
        app_id = request.form.get('application_id')
        if app_id:
            update_application(app_id, app_data)
            flash("Application updated!", "success")
        else:
            create_application(app_data)
            flash("Application tracked!", "success")
        return redirect(url_for('applications'))

    return render_template('applications.html', 
                           applications=get_all_applications(),
                           jobs=get_all_jobs(), # Needed for the dropdown
                           edit_mode=app_to_edit)

@app.route('/applications/delete/<int:id>')
def delete_application_route(id):
    delete_application(id)
    flash("Application deleted.", "danger")
    return redirect(url_for('applications'))



# --- CONTACTS ---
@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    edit_id = request.args.get('edit')
    contact_to_edit = None
    if edit_id:
        contact_to_edit = get_contact_by_id(edit_id)

    if request.method == 'POST':
        contact_data = {
            'company_id': request.form.get('company_id'),
            'name': request.form.get('contact_name'),
            'title': request.form.get('title'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'linkedin': request.form.get('linkedin_url'),
            'notes': request.form.get('notes')
        }
        
        contact_id = request.form.get('contact_id')
        if contact_id:
            update_contact(contact_id, contact_data)
            flash(f"Contact '{contact_data['name']}' updated!", "success")
        else:
            create_contact(contact_data)
            flash(f"Contact '{contact_data['name']}' added!", "success")
        return redirect(url_for('contacts'))

    return render_template('contacts.html', 
                           contacts=get_all_contacts(),
                           companies=get_all_companies(),
                           edit_mode=contact_to_edit)

@app.route('/contacts/delete/<int:id>')
def delete_contact_route(id):
    delete_contact(id)
    flash("Contact removed.", "danger")
    return redirect(url_for('contacts'))


# -- MATCHING JOB ---
@app.route('/match', methods=['GET', 'POST'])
def job_match():
    results = []
    user_skills = ""
    
    if request.method == 'POST':
        user_skills = request.form.get('skills', '')
        # Clean user input into a set of lowercase skills
        user_skills_set = {s.strip().lower() for s in user_skills.split(',') if s.strip()}
        
        all_jobs = get_all_jobs_for_matching()
        
        for job in all_jobs:
            # Parse the JSON requirements from the DB
            job_reqs = json.loads(job['requirements']) if job['requirements'] else []
            job_reqs_set = {r.lower() for r in job_reqs}
            
            if not job_reqs_set:
                continue
                
            # Find the intersection (matches)
            matches = user_skills_set.intersection(job_reqs_set)
            missing = job_reqs_set - user_skills_set
            
            match_percent = round((len(matches) / len(job_reqs_set)) * 100)
            
            results.append({
                'job_title': job['job_title'],
                'company': job['company_name'],
                'percent': match_percent,
                'matched_skills': list(matches),
                'missing_skills': list(missing)
            })
            
        # Sort results by percentage (highest first)
        results = sorted(results, key=lambda x: x['percent'], reverse=True)

    return render_template('job_match.html', results=results, user_skills=user_skills)

if __name__ == '__main__':
    app.run(debug=True)