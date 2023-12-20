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
        categories = cursor.execute("SELECT name FROM categories_{}".format(username)).fetchall()
        existing_categories = [category[0].strip() for category in categories]
        if not existing_categories:
            st.warning("No categories found. Please add categories first.")
            return
        selected_category=st.selectbox("Select Category", existing_categories)
        
        wallets = cursor.execute("SELECT DISTINCT wallet_name FROM wallets WHERE username=?", (username,)).fetchall()
        wallets = [wallet[0] for wallet in wallets]
        selected_wallet = st.selectbox('Wallet', wallets)
        
        label = st.selectbox('Label', ['Required.', 'Could be prevented.', 'Not needed.'])
        
        #New balance calculation
        balance = cursor.execute("SELECT amount FROM wallets WHERE username=? AND wallet_name=?", (username, selected_wallet)).fetchone()
        if balance:
            balance = balance[0]
        else:
            st.error(f"Wallet '{selected_wallet}' not found.")
            return
    
        updated_balance= balance-amount
        
        submit_button = st.form_submit_button("Add Transaction")

        if submit_button:
            # Include the username, wallet, and balance when inserting into the expenses table
            cursor.execute("INSERT INTO expenses (transaction_id, username, amount, date, reason, category, label, balance) VALUES (?, ?, ?, ?, ?, ?, ?,?)",
                           (transaction_id, username, amount, date, reason, selected_category, label, updated_balance))
            
            # Update the wallet balance in the wallets table
            cursor.execute("UPDATE wallets SET amount=? WHERE username=? AND wallet_name=?", (updated_balance, username, selected_wallet))
            conn.commit()
            
            st.success("Transaction added successfully!")

    # Close the database connection
    conn.close()



# Call the function to run the app