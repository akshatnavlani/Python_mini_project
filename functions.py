import random
import string
import streamlit as st
from datetime import datetime
import sqlite3 


#--------------db init--------

#-------------db init close---------------


#---------------Add Transaction----------------------
conn = sqlite3.connect("expense_db.db")
cursor = conn.cursor()

def is_transaction_id_unique(transaction_id, cursor):
    cursor.execute("SELECT COUNT(*) FROM expenses WHERE transaction_id = ?", (transaction_id,))
    count = cursor.fetchone()[0]
    return count == 0

def generate_unique_transaction_id(cursor):
    while True:
        transaction_id = ''.join(random.choice(string.digits) for i in range(6))
        if is_transaction_id_unique(transaction_id, cursor):
            return transaction_id
        

def add_transaction(username):
    # Connect to the database
    conn = sqlite3.connect("expense_db.db")
    cursor = conn.cursor()

    with st.form(key='add_transaction_form'):
        transaction_id = generate_unique_transaction_id(cursor)
        amount = st.number_input('Amount', value=0.0, step=10.0)
        date = st.date_input('Date', value=datetime.now())
        reason = st.text_input('Reason')
        categories = cursor.execute("SELECT name FROM categories").fetchall()
        categories = [category[0] for category in categories]
        category = st.selectbox('Category', categories)
        label = st.selectbox('Label', ['Required.', 'Could be prevented.', 'Not needed.'])
        
        submit_button = st.form_submit_button("Add Transaction")

        if submit_button:
            # Include the username when inserting into the expenses table
            cursor.execute("INSERT INTO expenses (transaction_id, username, amount, date, reason, category, label) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (transaction_id, username, amount, date, reason, category, label))
            conn.commit()
            st.success("Transaction added successfully!")

    # Close the database connection
    conn.close()


# Call the function to run the app