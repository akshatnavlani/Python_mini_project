import streamlit as st
import sqlite3
import base64

# Function to create or load user data
def create_user_data():
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        ''')
        print("Table 'users' created successfully.")
    except sqlite3.Error as e:
        print("Error creating 'users' table:", e)

    conn.commit()
    conn.close()

# Function to encode a password using base64
def encode_password(password):
    return base64.b64encode(password.encode('utf-8')).decode('utf-8')

# Function to sign up a new user
def sign_up(username, password):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        conn.close()
        return False, "Username already exists. Please choose a different username."
    else:
        try:
            encoded_password = encode_password(password)
            
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encoded_password))
            conn.commit()
            conn.close()
            return True, "Sign up successful. You can now log in."
        except sqlite3.Error as e:
            conn.close()
            return False, "Error during signup. Please try again."

# Function to verify a password using base64
def verify_password(input_password, encoded_password):
    stored_password = base64.b64decode(encoded_password).decode('utf-8')
    return stored_password == input_password

# Function to log in an existing user
def log_in(username, password):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user_data = cursor.fetchone()

    if user_data:
        if verify_password(password, user_data[2]):
            conn.close()
            return True, "Login successful."
        else:
            conn.close()
            return False, "Incorrect password. Please try again."
    else:
        conn.close()
        return False, "Username not found. Please sign up."

# Main function
def main():
    st.title("Expense Tracker App")

    # Create or load user data
    create_user_data()

    # Initialize 'authenticated' attribute in the session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # Sidebar for user authentication
    st.sidebar.header("User Authentication")

    # Sign Up Form
    with st.sidebar.form("sign_up_form"):
        st.write("### Sign Up")
        new_username = st.text_input("New Username:")
        new_password = st.text_input("New Password:", type="password", key="signup_password")

        if st.form_submit_button("Sign Up"):
            success, message = sign_up(new_username, new_password)
            if success:
                st.session_state.authenticated = True
                st.success(message)
            else:
                st.error(message)

    # Log In Form
    with st.sidebar.form("log_in_form"):
        st.write("### Log In")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        if st.form_submit_button("Log In"):
            success, message = log_in(username, password)
            if success:
                st.session_state.authenticated = True
                st.success(message)
            else:
                st.error(message)

# Run the app
if __name__ == "__main__":
    main()


