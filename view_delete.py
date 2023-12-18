import sqlite3
import streamlit as st
import pandas as pd

def view_transactions():

    conn = sqlite3.connect("expense_db.db")

    transactions = pd.read_sql_query("SELECT transaction_id, amount, date, reason, category, label FROM expenses", conn)

    st.title("All Transactions")

    if not transactions.empty:
        table_container = st.empty()

        transactions_display = transactions[['transaction_id', 'amount', 'date', 'reason', 'category', 'label']].reset_index(drop=True)

        table_container.dataframe(transactions_display, use_container_width=True)


        selected_transactions = st.multiselect("Select transactions to delete", transactions['transaction_id'].tolist())

        # Delete button
        if st.button("Delete Selected Transactions"):
            for transaction_id in selected_transactions:
                delete_transaction(conn, transaction_id)

        updated_transactions = pd.read_sql_query("SELECT transaction_id, amount, date, reason, category, label FROM expenses", conn)
        updated_transactions_display = updated_transactions[['transaction_id', 'amount', 'date', 'reason', 'category', 'label']].reset_index(drop=True)
        table_container.dataframe(updated_transactions_display, use_container_width=True)

    else:
        st.warning("No transactions found.")

    conn.close()

def delete_transaction(conn, transaction_id):
    conn.execute(f"DELETE FROM expenses WHERE transaction_id = '{transaction_id}'")
    conn.commit()
    st.success(f"Transaction {transaction_id} deleted successfully.")

view_transactions()
