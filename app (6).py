import sqlite3
from datetime import date

import pandas as pd
import streamlit as st

DB_FILE = "employees.db"


# ---------- Database helpers ----------
def get_connection():
    return sqlite3.connect(DB_FILE)


def create_table():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS employees (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                email       TEXT UNIQUE NOT NULL,
                phone       TEXT,
                department  TEXT,
                designation TEXT,
                salary      REAL,
                join_date   TEXT
            )
            """
        )


def add_employee(name, email, phone, department, designation, salary, join_date):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO employees
            (name, email, phone, department, designation, salary, join_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (name, email, phone, department, designation, salary, str(join_date)),
        )


def get_employees(search=""):
    query = "SELECT * FROM employees"
    params = ()
    if search:
        query += " WHERE name LIKE ? OR department LIKE ? OR designation LIKE ?"
        params = (f"%{search}%",) * 3
    with get_connection() as conn:
        return pd.read_sql_query(query + " ORDER BY id DESC", conn, params=params)


def delete_employee(emp_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM employees WHERE id = ?", (emp_id,))


# ---------- Page setup ----------
st.set_page_config(page_title="Employee Management", page_icon="👥", layout="wide")
create_table()

st.title("👥 Employee Management System")
page = st.sidebar.radio("Menu", ["Add Employee", "View Employees"])

# ---------- Add Employee ----------
if page == "Add Employee":
    st.subheader("Add New Employee")

    with st.form("add_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("Full Name *")
        email = col2.text_input("Email *")
        phone = col1.text_input("Phone")
        department = col2.selectbox(
            "Department", ["HR", "IT", "Finance", "Sales", "Marketing", "Operations"]
        )
        designation = col1.text_input("Designation")
        salary = col2.number_input("Salary", min_value=0.0, step=1000.0)
        join_date = col1.date_input("Joining Date", value=date.today())

        submitted = st.form_submit_button("Save Employee")

    if submitted:
        if not name.strip() or not email.strip():
            st.error("Name and Email are required.")
        else:
            try:
                add_employee(
                    name.strip(), email.strip(), phone, department,
                    designation, salary, join_date,
                )
                st.success(f"✅ {name} was added successfully!")
            except sqlite3.IntegrityError:
                st.error("An employee with this email already exists.")

# ---------- View Employees ----------
else:
    st.subheader("Employee Records")
    search = st.text_input("🔍 Search by name, department or designation")
    df = get_employees(search)

    st.metric("Total Employees", len(df))

    if df.empty:
        st.info("No employee records found.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.download_button(
            "⬇️ Download as CSV",
            df.to_csv(index=False).encode("utf-8"),
            "employees.csv",
            "text/csv",
        )

        with st.expander("Delete an employee"):
            emp_id = st.selectbox(
                "Select employee",
                df["id"],
                format_func=lambda i: f"{i} - {df.loc[df['id'] == i, 'name'].iloc[0]}",
            )
            if st.button("Delete"):
                delete_employee(emp_id)
                st.success("Employee deleted.")
                st.rerun()
