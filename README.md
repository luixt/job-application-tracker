# Job Application Tracker

A web application to help track job applications during the job
search process.

## Features (Coming Soon)
- Track companies and job listings
- Record application submissions
- Manage interview schedules
- Store contact information

## Technologies
- MySQL Database
- Python with Flask
- HTML/CSS for the web interface

## Testing

### 1. Database Setup
1. Install MySQL Server.
2. Run the schema script to create the database and tables:
   - **macOS/Linux:** `mysql -u root -p < schema.sql`
   - **Windows:** `mysql -u root -p < schema.sql` (Ensure MySQL is in your System PATH)

### 2. Environment Variable (.env)

Create a file named .env in the root directory and add your database credentials:

```plaintext
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=job_tracker
```

### 3. Python Environment Setup
#### macOS / Linux
```bash
# Create virtual environment
python3 -m venv venv
# Activate it
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

#### Windows
```bash
# Create virtual environment
python -m venv venv
# Activate it
.\venv\Scripts\activate
# Install dependencies
pip install -r requirements.txt
```

### 4. Running the Application
Once the database is set up and the environment is active:

1. Run the program:

```Bash
Python app.py
```

2. Open your browser and navigate to: http://127.0.0.1:5000