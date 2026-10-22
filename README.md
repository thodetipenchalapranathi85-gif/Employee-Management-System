# Employee Management System

A simple application to store and manage employee details. You can add employees, view them in a table, search them, and delete them.

It comes in two versions:

| Version | File | Storage |
|---|---|---|
| Web page | `employee-app.html` | Browser storage (`localStorage`) |
| Python app | `app.py` | SQLite database (`employees.db`) |

## Features

- Add employee details: name, email, phone, department, designation, salary, joining date
- Name and email are required; duplicate emails are rejected
- View all records in a table with a total count
- Search by name, department or designation
- Delete employee records
- Data is saved and still there after the app is closed
- CSV download (Python version only)

## Project Structure

```
employee_app/
├── app.py              # Python + Streamlit + SQLite app
├── employee-app.html   # Stand-alone web page
├── requirements.txt    # Python libraries
├── README.md           # This file
└── employees.db        # Created automatically on first run
```

## Run the Web Page Version

1. Download `employee-app.html`.
2. Double-click it to open it in Chrome, Edge or Firefox.

No installation is needed. Data is stored only in that browser on that device.

## Run the Python Version

**Requirements:** Python 3.9 or newer.

1. Put `app.py` and `requirements.txt` in one folder.
2. Open a terminal in that folder.
3. Install the libraries:
   ```
   pip install -r requirements.txt
   ```
4. Start the app:
   ```
   streamlit run app.py
   ```
5. Your browser opens at `http://localhost:8501`.

## Database Table

The database file `employees.db` has one table called `employees`:

| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Primary key, automatic |
| name | TEXT | Required |
| email | TEXT | Required, unique |
| phone | TEXT | Optional |
| department | TEXT | HR, IT, Finance, Sales, Marketing, Operations |
| designation | TEXT | Job title |
| salary | REAL | Salary amount |
| join_date | TEXT | Date of joining |

## Technologies Used

- Python, Streamlit, Pandas, SQLite (`sqlite3`)
- HTML, CSS, JavaScript

## Future Improvements

- Edit or update employee details
- Admin login
- Attendance tracking (Present, Absent, Late) with daily, weekly and monthly reports
- Charts by department
