-- Create the Database
CREATE DATABASE IF NOT EXISTS job_tracker;
USE job_tracker;

CREATE TABLE companies (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    website VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    notes TEXT
);

-- (Depends on companies)
CREATE TABLE jobs (
    job_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    job_title VARCHAR(100) NOT NULL,
    job_type ENUM('Full-time', 'Part-time', 'Contract', 'Internship'),
    salary_min INT,
    salary_max INT,
    job_url VARCHAR(300),
    date_posted DATE,
    requirements JSON,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- (Depends on companies)
CREATE TABLE contacts (
    contact_id INT PRIMARY KEY AUTO_INCREMENT,
    company_id INT,
    contact_name VARCHAR(100) NOT NULL,
    title VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    linkedin_url VARCHAR(200),
    notes TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE CASCADE
);

-- (Depends on jobs)
CREATE TABLE applications (
    application_id INT PRIMARY KEY AUTO_INCREMENT,
    job_id INT,
    application_date DATE NOT NULL,
    status ENUM('Applied', 'Screening', 'Interview', 'Offer', 'Rejected', 'Withdrawn') DEFAULT 'Applied',
    resume_version VARCHAR(50),
    cover_letter_sent BOOLEAN DEFAULT FALSE,
    interview_data JSON,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id) ON DELETE CASCADE
);

-- TESTING DATA
-- 1. Insert 5 Companies
INSERT INTO companies (company_name, industry, website, city, state, notes) VALUES
('TechCorp Solutions', 'Software Development', 'https://techcorp.example.com', 'San Francisco', 'CA', 'Leading provider of cloud infrastructure.'),
('DataCo Analytics', 'Data Science', 'https://dataco.example.com', 'Austin', 'TX', 'Specializes in AI-driven market insights.'),
('HealthFirst Systems', 'Healthcare Tech', 'https://healthfirst.example.com', 'Miami', 'FL', 'Focused on telemedicine and patient portals.'),
('GreenEnergy Inc', 'Renewable Energy', 'https://greenenergy.example.com', 'Denver', 'CO', 'Building smart grids for solar energy.'),
('FinanceFlow', 'Fintech', 'https://financeflow.example.com', 'New York', 'NY', 'Disrupting traditional banking with blockchain.');

-- 2. Insert 5 Jobs (Linked to Companies)
-- Note: Requirements are stored as JSON arrays for the Job Matcher
INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements) VALUES
(1, 'Software Developer', 'Full-time', 110000, 150000, 'https://techcorp.example.com/careers/sw-dev', '2024-03-01', '["Python", "Flask", "MySQL", "Docker"]'),
(2, 'Data Analyst', 'Full-time', 85000, 115000, 'https://dataco.example.com/jobs/data-analyst', '2024-03-05', '["SQL", "Python", "Tableau", "Excel"]'),
(3, 'Backend Engineer', 'Contract', 90000, 130000, 'https://healthfirst.example.com/openings/backend', '2024-03-10', '["Python", "Flask", "AWS", "Redis"]'),
(4, 'Frontend Intern', 'Internship', 45000, 55000, 'https://greenenergy.example.com/internships', '2024-03-15', '["HTML", "CSS", "JavaScript", "React"]'),
(5, 'Database Administrator', 'Full-time', 100000, 140000, 'https://financeflow.example.com/jobs/dba', '2024-03-20', '["MySQL", "SQL", "Security", "Linux"]');

-- 3. Insert 5 Networking Contacts (Linked to Companies)
INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes) VALUES
(1, 'Jane Smith', 'Senior Recruiter', 'jane.smith@techcorp.example.com', '555-0101', 'https://linkedin.com/in/janesmith-example', 'Met at the 2024 Tech Expo. Very friendly.'),
(2, 'Michael Chen', 'Lead Data Scientist', 'm.chen@dataco.example.com', '555-0102', 'https://linkedin.com/in/mchen-data', 'Spoke about their AI project on LinkedIn.'),
(3, 'Sarah Johnson', 'HR Manager', 'sjohnson@healthfirst.example.com', '555-0103', 'https://linkedin.com/in/sjohnson-health', 'Referred by a former colleague.'),
(4, 'David Rodriguez', 'Engineering Lead', 'd.rodriguez@greenenergy.example.com', '555-0104', 'https://linkedin.com/in/drodriguez-green', 'Interested in candidates with smart grid experience.'),
(5, 'Emily White', 'Talent Acquisition', 'ewhite@financeflow.example.com', '555-0105', 'https://linkedin.com/in/ewhite-fintech', 'Sent a cold message, she responded quickly.');

-- 4. Insert 5 Applications (Linked to Jobs)
INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data) VALUES
(1, '2024-03-02', 'Interview', 'Tech_Dev_v2', 1, '{"round": 1, "interviewer": "Jane Smith"}'),
(2, '2024-03-06', 'Screening', 'Data_Analyst_Final', 1, '{}'),
(5, '2024-03-21', 'Applied', 'DBA_Resume_2024', 1, '{}'),
(3, '2024-03-11', 'Rejected', 'Generic_Backend', 0, '{}'),
(4, '2024-03-16', 'Offer', 'Frontend_Intern_v1', 1, '{"notes": "Salary negotiation in progress"}');