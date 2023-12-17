import sqlite3 
import streamlit as st  
import random_transaction_id
from datetime import datetime

def add_transaction():
    # Connect to the database
    conn = sqlite3.connect("expense_db.db")
    cursor = conn.cursor()

    with st.form(key='add_transaction_form'):
        transaction_id = random_transaction_id.generate_unique_transaction_id(cursor)
        amount = st.number_input('Amount', value=0.0, step=10.0)
        date = st.date_input('Date', value=datetime.now())
        reason = st.text_input('Reason')
        categories = cursor.execute("SELECT name FROM categories").fetchall()
        categories = [category[0] for category in categories]
        category = st.selectbox('Category', categories)
        label = st.selectbox('Label', ['Required.', 'Could be prevented.', 'Not needed.'])
        
        submit_button = st.form_submit_button("Add Transaction")

        if submit_button:
            cursor.execute("INSERT INTO expenses (transaction_id, amount, date, reason, category, label) VALUES (?, ?, ?, ?, ?, ?)",
                           (transaction_id, amount, date, reason, category, label))
            conn.commit()
            st.success("Transaction added successfully!")

    # Close the database connection
    conn.close()

# Call the function to run the app
add_transaction()