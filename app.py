from flask import Flask, render_template, request, redirect, flash, url_for
# Import all our data functions from database.py
from database import (
    get_dashboard_stats, get_recent_applications, get_all_companies, 
    create_company, get_company_by_id, update_company, delete_company
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