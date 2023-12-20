
import sqlite3
import streamlit as st
import pandas as pd

# Initialize session state
if 'username' not in st.session_state:
    st.session_state.username = None  # Set a default value or initialize it based on your application logic



def view_transactions(username):

    conn = sqlite3.connect("expense_db.db")

    transactions_query = f"SELECT transaction_id, amount, date, reason, category, label FROM expenses WHERE username = '{username}'"
    transactions = pd.read_sql_query(transactions_query, conn)

    st.title("Your Transactions")

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
        st.warning("No transactions found for your account.")

    conn.close()

def delete_transaction(conn, transaction_id):
    conn.execute(f"DELETE FROM expenses WHERE transaction_id = '{transaction_id}'")
    conn.commit()
    st.success(f"Transaction {transaction_id} deleted successfully.")

# Assuming you have the current username stored in st.session_state.username
    
view_transactions(st.session_state.username)
