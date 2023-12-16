import streamlit as st
import sqlite3
import base64

# Global variable to track if user data has been created
user_data_initialized = False

# Function to create or load user data
def create_user_data():
    user_data_initialized = False

    # Create or load user data
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    try:
        # Create 'users' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        ''')
        print("Table 'users' created successfully.")

        # Create 'expenses' table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                description TEXT,
                date TEXT,
                category TEXT,  -- Add the 'category' column
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        print("Table 'expenses' created successfully.")

        user_data_initialized = True
    except sqlite3.Error as e:
        print("Error creating tables:", e)

    conn.commit()
    conn.close()


# Function to encode a password using base64
def encode_password(password):
    return base64.b64encode(password.encode('utf-8')).decode('utf-8')

# Function to sign up a new user
def sign_up(username, password):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    print("whooooooo")
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
            print("Sign up successful. You can now log in.")
            return True, "Sign up successful. You can now log in."
        except sqlite3.Error as e:
            conn.close()
            print("Error during signup:", e)
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
            return True, user_data[0], "Login successful."
        else:
            conn.close()
            return False, user_data[0], "Incorrect password. Please try again."
    else:
        conn.close()
        return False, None, "Username not found. Please sign up."



