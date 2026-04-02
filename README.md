# Job Application Tracker

A comprehensive full-stack web application designed to organize and optimize the job search process, featuring a relational database and a skill-matching engine.

## 🚀 Features
- **Company Management**: Track industries, locations, and personal notes for target employers.
- **Job Listings**: Log roles, salary ranges, and technical requirements.
- **Application Tracking**: Monitor the status of every application (Applied, Interview, Offer, etc.) with resume version tracking.
- **Networking Contacts**: Store key contacts, LinkedIn profiles, and emails linked to specific companies.
- **Job Match Engine**: Algorithmic matching that compares your skills against job requirements to calculate a match percentage.

## 🛠️ Technologies
- **Backend**: Python 3 with Flask
- **Database**: MySQL 8.0+
- **Frontend**: HTML, CSS (Custom responsive design)

## ⚙️ Setup & Installation (Testing)

### 1. Database Setup
1. Clone the Repository. Ensure you have install MySQL Server and it is running.

2. Open the terminal, navigate to the project root folder ```bash /Job-Application-Tracker```, and run the schema script to create the database and tables:
   - **macOS/Linux:** `mysql -u root -p < schema.sql`
   - **Windows:** `mysql -u root -p < schema.sql` (Ensure MySQL is in your System PATH)

#### 💡 Troubleshooting Note

Stuck on "Command Not Found"? > If your terminal doesn't recognize pip, python, or mysql, use an AI assistant to help you add these tools to your system's PATH. Simply paste the error you're seeing, and it will guide you through the specific steps for your OS.

### 2. Environment Variable (.env)

Create a file named .env in the root directory and add your database credentials:

```plaintext
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=job_tracker
```

### 3. Python Environment Setup
Open the terminal and run the commands:

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
#### macOS / Linux
```Bash
Python3 app.py
```

#### Windows
```Bash
Python app.py
```

2. Open your browser and navigate to: http://127.0.0.1:5000
