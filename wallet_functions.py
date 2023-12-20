import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def add_wallet(conn):
    cursor = conn.cursor()

    st.header("Add Wallet")

    new_wallet = st.text_input("New Wallet")
    add_wallet_button = st.button("Add Wallet")

    success_message_shown = False

    if add_wallet_button and new_wallet:
        cursor.execute("INSERT OR REPLACE INTO wallets (wallet_name, username, amount) VALUES (?,?,?)", (new_wallet, st.session_state.username, 0.0))
        conn.commit()
        success_message_shown = True

    if success_message_shown:
        st.success(f"Wallet '{new_wallet}' added or updated successfully!")
        st.rerun()
        
        
def set_initial_wallet_amount(username, conn):
    cursor = conn.cursor()

    st.header("Set Initial Wallet Amount")

    # Display existing wallets
    existing_wallets = cursor.execute("SELECT DISTINCT wallet_name FROM wallets WHERE username=?", (username,)).fetchall()
    existing_wallets = [wallet[0] for wallet in existing_wallets]

    if not existing_wallets:
        st.warning("No wallets found. Please add wallets first.")
        return

    selected_wallet = st.selectbox("Select Wallet", existing_wallets)

    # Display current balance (if available)
    current_balance = cursor.execute("SELECT amount FROM wallets WHERE username=? AND wallet_name=?", (username, selected_wallet)).fetchone()
    if current_balance:
        current_balance = current_balance[0]
        st.write(f"Current Balance for '{selected_wallet}': ₹{current_balance:.2f}")

    # Set initial amount
    initial_amount = st.number_input("Enter Initial Amount", min_value=0.0, value=current_balance or 0.0, step=100.0)

    set_amount_button = st.button("Set Initial Amount")

    if set_amount_button:
        # Update the wallet amount
        cursor.execute("UPDATE wallets SET amount = ? WHERE username = ? AND wallet_name = ?",
                       (initial_amount, username, selected_wallet))
        conn.commit()
        st.success(f"Initial amount for '{selected_wallet}' set successfully!")
        st.experimental_rerun()
      
def display_wallet_table(username, conn):
    wallet_query = f"SELECT wallet_name, amount FROM wallets WHERE username = '{st.session_state.username}'"
    wallets = pd.read_sql_query(wallet_query, conn)

    if not wallets.empty:
        st.header("Wallets")
        st.table(wallets)
    else:
        st.warning("No wallets found.")


def delete_wallet(conn):
    cursor = conn.cursor()

    st.header("Delete Wallet")

    delete_wallet = st.text_input("Delete Wallet")
    delete_wallet_button = st.button("Delete Wallet")

    if delete_wallet_button and delete_wallet:
        cursor.execute("DELETE FROM wallets WHERE wallet_name=? AND username=?", (delete_wallet, st.session_state.username))
        conn.commit()
        st.success(f"Wallet '{delete_wallet}' deleted successfully!")
        st.rerun()

def calculate_total_wallet_amount(username, cursor):
    cursor.execute("SELECT DISTINCT wallet_name FROM wallets WHERE username=?", (username,))
    wallet_names = [row[0] for row in cursor.fetchall()]

    total_amount = 0
    for wallet_name in wallet_names:
        cursor.execute("SELECT SUM(amount) FROM wallets WHERE username=? AND wallet_name=?", (username, wallet_name))
        total_amount += cursor.fetchone()[0] or 0

    return total_amount

def calculate_total_expenses(username, interval, cursor):
    current_date = datetime.now().date()

    if interval == "monthly":
        start_date = datetime(current_date.year, current_date.month, 1).date()
    elif interval == "daily":
        start_date = current_date
    elif interval == "weekly":
        start_date = current_date - timedelta(days=current_date.weekday())
    else:
        return 0  # Invalid interval

    end_date = current_date  # Set end date to the current date for monthly and daily intervals

    cursor.execute("SELECT SUM(amount) FROM expenses WHERE username=? AND date>=? AND date<=?", (username, start_date, end_date))
    total_amount = cursor.fetchone()[0] or 0

    return total_amount


