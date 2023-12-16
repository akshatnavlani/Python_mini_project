import sqlite3
import pandas as pd
import streamlit as st

# Function to ADD expenses
def add_expenses(user_id, income, expenses, description, date, category):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO expenses (user_id, income, expenses, description, date, category) VALUES (?,?,?,?,?)",
                       (user_id, income, expenses, description, date, category))
        conn.commit()
        conn.close()
        return True, "Expense added successfully."
    except sqlite3.Error as e:
        conn.close()
        return False, f"Error adding expense: {e}"

      
# Function to VIEW Expenses
def view_expenses(user_id, date=None):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    if date:
        cursor.execute("SELECT id, user_id, income, expenses, description, date, category FROM expenses WHERE user_id=? AND date=?", (user_id, date))
    else:
        cursor.execute("SELECT id, user_id, income, expenses, description, date, category FROM expenses WHERE user_id=?", (user_id,))

    expenses = cursor.fetchall()
    conn.close()
    return expenses

# Function to MODIFY expenses
def modify_expenses(expense_id, income, expenses, description, date):
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE expenses SET income=?, expenses=?, description=?, date=? WHERE id=?",
                       (income, expenses, description, date, expense_id))
        conn.commit()
        conn.close()
        return True, "Expense modified successfully."
    except sqlite3.Error as e:
        conn.close()
        return False, f"Error modifying expense: {e}"

# FUnction to DISPLAY Expenses catergory wise
def display_expenses(expenses, title):
    if expenses:
        st.header(title)
        df = pd.DataFrame(expenses, columns=["Expense ID", "User ID", "Income","Expenses", "Description", "Date", "Category"])
        st.dataframe(df)
    else:
        st.info("No expenses found for the selected period.")
