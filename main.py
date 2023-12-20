import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256
import add_transactions
import categories
import view_delete
import pandas as pd
import wallet_functions


# Create a connection to the SQLite database
conn = sqlite3.connect("expense_db.db")

# Use a context manager for database operations
with conn:
    # Create a cursor within the context manager
    cursor = conn.cursor()

    # Create the users table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            name TEXT,
            password TEXT
        )
    ''')

    # Create the expenses table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            transaction_id TEXT PRIMARY KEY,
            username TEXT,
            amount REAL,
            date TEXT,
            reason TEXT,
            category TEXT,
            label TEXT,
            balance REAL -- Add the 'balance' column
        )
    ''')

    # Create the categories table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            name TEXT PRIMARY KEY,
            color TEXT
        )
    ''')

    # Create the wallets table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS wallets (
            wallet_id TEXT PRIMARY KEY,
            username TEXT,
            wallet_name TEXT,
            amount REAL,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    ''')
#conn.commit()


# Initialize session_state
if "username" not in st.session_state:
    st.session_state.username = None
if "show_signup" not in st.session_state:
    st.session_state.show_signup = False
if "signup_name" not in st.session_state:
    st.session_state.signup_name = None
    

# Main content
if not st.session_state.username:
    st.title("Login")

    # Login form
    username = st.text_input("Username",key="login_username")
    password = st.text_input("Password", type="password", key="login_passsword")

    if st.button("Login"):
        # Check if the entered credentials are valid
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

        if user and pbkdf2_sha256.verify(password, user[2]):
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

    st.text("Don't have an account?")
    if st.button("Sign Up"):
        st.session_state.show_signup = not st.session_state.show_signup

# Hide the signup form after login
if st.session_state.username and st.session_state.show_signup:
    st.session_state.show_signup = False

# Display the main app content after successful login
if st.session_state.username and not st.session_state.show_signup:
    # Fetch the user from the database based on the logged-in username
    cursor.execute("SELECT * FROM users WHERE username=?", (st.session_state.username,))
    user = cursor.fetchone()
    if user:
        # Sidebar
        st.sidebar.title("Expense Tracker")
        st.sidebar.write(f"Welcome, {user[1]}!")
        st.sidebar.button("Logout", on_click=lambda: setattr(st.session_state, "username", None))
        # Your existing app content goes here

#--------------------------------APP CONTENT------------------------------------
        page = st.sidebar.radio("Select a page", ["Home", "Add Transaction", "Manage Categories","View Transactions","Wallet"])
        
        if page == "Home":
            st.title("Home")
            
            # Calculate and display total amount in wallet
            total_wallet_amount = wallet_functions.calculate_total_wallet_amount(st.session_state.username, cursor)
            st.info(f"Amount in Wallet: ₹{total_wallet_amount:.2f}")
    
            # Calculate and display total expenses this month
            total_expenses_monthly = wallet_functions.calculate_total_expenses(st.session_state.username, "monthly", cursor)
            st.info(f"Total Expenses This Month: ₹{total_expenses_monthly:.2f}")
            
        elif page == "Add Transaction":
            st.title("Add Transaction")
            add_transactions.add_transaction(st.session_state.username)

        elif page == "Manage Categories":
            st.title("Manage Categories")
            categories.main()
            
        elif page == "View Transactions":
            st.title("View Transactions")
            view_delete.view_transactions(st.session_state.username)
            
        elif page== "Wallet":
            st.title("Wallet")
            wallet_functions.display_wallet_table(st.session_state.username, conn)    
            wallet_functions.add_wallet(conn)
            wallet_functions.set_initial_wallet_amount(st.session_state.username, conn)
            wallet_functions.delete_wallet(conn)
#--------------------------------APP CONTENT END-----------------------------


# Display the signup form
if st.session_state.show_signup:
    st.title("Sign Up")

    new_username = st.text_input("New Username")
    st.session_state.signup_name = st.text_input("Full Name")  # Store the name in session_state
    new_password = st.text_input("New Password", type="password")

    if st.button("Create Account"):
        # Check if the username is already taken
        cursor.execute("SELECT * FROM users WHERE username=?", (new_username,))
        existing_user = cursor.fetchone()

        if existing_user:
            st.error("Username already taken. Choose a different one.")
        else:
            # Insert the new user into the database
            hashed_password = pbkdf2_sha256.hash(new_password)
            cursor.execute("INSERT INTO users (username, name, password) VALUES (?, ?, ?)",
                           (new_username, st.session_state.signup_name, hashed_password))
            conn.commit()
            st.success("Account created successfully! Please login.")

# Close the database connection
conn.close()
