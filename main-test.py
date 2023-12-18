import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256

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
@st.cache_data(allow_output_mutation=True)
def get_login_status():
    return st.session_state.username

if not get_login_status():
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
        else:
            st.error("Invalid credentials")

    st.text("Don't have an account?")
    if st.button("Sign Up"):
        st.session_state.show_signup = not st.session_state.show_signup

# Hide the signup form after login
if get_login_status() and st.session_state.show_signup:
    st.session_state.show_signup = False

# Display the main app content after successful login
if get_login_status():
    st.title("Main App")

    # Sidebar with navigation links
    st.sidebar.title("Navigation")

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.username = None

    # Fetch the user from the database based on the logged-in username
    cursor.execute("SELECT * FROM users WHERE username=?", (get_login_status(),))
    user = cursor.fetchone()
    if user:
        st.write(f"Welcome, {user[1]}!")

        # Additional pages that should be visible only after login
        page = st.sidebar.radio("Select a page", ["Home", "Page 1", "Page 2"])

        if page == "Home":
            st.title("Home")
            st.write("This is the home page.")

        elif page == "Page 1":
            st.title("Page 1")
            st.write("This is Page 1.")

        elif page == "Page 2":
            st.title("Page 2")
            st.write("This is Page 2.")

# Display the signup form
if not get_login_status() and st.session_state.show_signup:
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
