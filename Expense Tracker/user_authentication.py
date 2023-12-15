import streamlit as st
import sqlite3
import base64

# Global variable to track if user data has been created
user_data_initialized = False

# Function to create or load user data
def create_user_data():
    global user_data_initialized
    
    if not user_data_initialized:
        # Create a connection and cursor for the 'users' table
        conn_users = sqlite3.connect('user_data.db')
        cursor_users = conn_users.cursor()
        
        try:
            cursor_users.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT
                )
            ''')
            print("Table 'users' created successfully.")
            user_data_initialized = True
        except sqlite3.Error as e:
            print("Error creating 'users' table:", e)

        conn_users.commit()
        conn_users.close()
        
        # Create a new connection and cursor for the 'expenses' table
        conn_expenses = sqlite3.connect('user_data.db')
        cursor_expenses = conn_expenses.cursor()
        
        try:
            cursor_expenses.execute('''
                CREATE TABLE IF NOT EXISTS expenses (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  amount REAL,
                  description TEXT,
                  date TEXT,
                  FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            print("Table 'expenses' created successfully.")
            user_data_initialized = True
        except sqlite3.Error as e:
            print("Error creating 'expenses' table:", e)

        conn_expenses.commit()
        conn_expenses.close()

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
        return False, user_data[0], "Username not found. Please sign up."




