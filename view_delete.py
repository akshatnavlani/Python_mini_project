import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime
from wallet_functions import calculate_total_expenses

# Initialize session_state
if 'username' not in st.session_state:
    st.session_state.username = None

def view_transactions(username):
    conn = sqlite3.connect("expense_db.db")
    cursor = conn.cursor()

    transactions_query = f"SELECT transaction_id, amount, date, reason, category, label FROM expenses WHERE username = '{username}'"

    
    selected_month_name = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], key="monthly_dropdown")
        
    # Check if a month is selected
    if selected_month_name:
        # Convert the month name to numeric representation
        selected_month_numeric = datetime.strptime(selected_month_name, '%B').strftime('%m')
            
        # Filter expenses for the selected month
        transactions_query = f"SELECT transaction_id, amount, date, reason, category, label FROM expenses WHERE username = '{username}' AND strftime('%m', date) = '{selected_month_numeric}' AND strftime('%Y', date) = strftime('%Y', 'now')"

    transactions = pd.read_sql_query(transactions_query, conn)

    if not transactions.empty:
        table_container = st.empty()

        transactions_display = transactions[['transaction_id', 'amount', 'date', 'reason', 'category', 'label']].reset_index(drop=True)

        table_container.dataframe(transactions_display, use_container_width=True)

        selected_transactions = st.multiselect("Select transactions to delete", transactions['transaction_id'].tolist())

        # Delete button
        if st.button("Delete Selected Transactions"):
            for transaction_id in selected_transactions:
                delete_transaction(conn, transaction_id)

            # Reload updated transactions after deletion
            updated_transactions = pd.read_sql_query(transactions_query, conn)
            updated_transactions_display = updated_transactions[['transaction_id', 'amount', 'date', 'reason', 'category', 'label']].reset_index(drop=True)
            table_container.dataframe(updated_transactions_display, use_container_width=True)
    else:
        st.warning("No transactions available for this month.")
        return
    
    conn.close()

def delete_transaction(conn, transaction_id):
    conn.execute(f"DELETE FROM expenses WHERE transaction_id = '{transaction_id}'")
    conn.commit()
    st.success(f"Transaction {transaction_id} deleted successfully.")

# Assuming you have the current username stored in st.session_state.username
view_transactions(st.session_state.username)
