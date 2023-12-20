import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256
import functions
import categories
# Create a connection to the SQLite database
conn = sqlite3.connect("expense_db.db")
cursor = conn.cursor()

# Create the users table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        name TEXT,
        password TEXT
    )
''')
conn.commit()

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
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

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
    st.title("Main App")
    # Fetch the user from the database based on the logged-in username
    cursor.execute("SELECT * FROM users WHERE username=?", (st.session_state.username,))
    user = cursor.fetchone()
    if user:
# Sidebar
        st.sidebar.title("Streamlit Auth Demo")
        st.sidebar.write(f"Welcome, {user[1]}!")
        st.sidebar.button("Logout", on_click=lambda: setattr(st.session_state, "username", None))
        # Your existing app content goes here


#--------------------------------APP CONTENT------------------------------------
        page = st.sidebar.radio("Select a page", ["Home", "Add Transaction", "Manage Categories","View Transactions"])
        if page == "Home":
            st.title("Home")
            st.write("This is the home page.")

        elif page == "Add Transaction":
            st.title("Add Transaction")
            functions.add_transaction()

        elif page == "Page 2":
            st.title("Page 2")
            categories.main()

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
