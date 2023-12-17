import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from user_authentication import create_user_data, log_in, sign_up
from expenses import add_expenses, view_expenses, modify_expenses, display_expenses

def main():
    st.title("Expense Tracker App")

    # Create or load user data
    create_user_data()

    # Initialize 'authenticated' and 'user_id' attributes in the session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None 

    # Sidebar for user authentication
    st.sidebar.header("User Authentication")

    # Log In Form in Sidebar
    with st.sidebar.form("log_in_form"):
        st.write("### Log In")
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        if st.form_submit_button("Log In"):
            success, user_id, message = log_in(username, password)
            if success:
                st.session_state.authenticated = True
                st.session_state.user_id = user_id
                st.success(message)
            else:
                st.error(message)

    # Sign Up Form in Sidebar
    with st.sidebar.form("sign_up_form"):
        st.write("### Sign Up")
        new_username = st.text_input("New Username:")
        new_password = st.text_input("New Password:", type="password", key="signup_password")

        if st.form_submit_button("Sign Up"):
            success, message = sign_up(new_username, new_password)
            if success:
                st.success(message)
            else:
                st.error(message)

    # Expense Module
    if st.session_state.authenticated:
        # Add Expense Form
        with st.form("add_expense_form"):
            st.write("### Add Expense")
            amount = st.number_input("Amount:",step=50)
            description = st.text_input("Description:")
            date = st.date_input("Date:")
            category = st.selectbox("Category:",("Education","Travel", "Food", "Entertainment", "Other"))  # Add a field for category

            if st.form_submit_button("Add Expense"):
                success, message = add_expenses(st.session_state.user_id, amount, description, date, category)
                if success:
                    st.success(message)
                else:
                    st.error(message)


        # View Expenses Buttons
        if st.button("View Daily Expenses", key="view_daily_expenses"):
            today = datetime.now().strftime('%Y-%m-%d')
            expenses = view_expenses(st.session_state.user_id, today)
            display_expenses(expenses, "Daily Expenses")

        if st.button("View Weekly Expenses", key="view_weekly_expenses"):
            today = datetime.now()
            expenses = view_expenses(st.session_state.user_id, today)
            display_expenses(expenses, "Weekly Expenses")

        if st.button("View Monthly Expenses", key="view_monthly_expenses"):
            today = datetime.now()
            expenses = view_expenses(st.session_state.user_id, today)
            display_expenses(expenses, "Monthly Expenses")
            
            
        # Modify Expense Form
        with st.form("modify_expense_form"):
            st.write("### Modify Expense")
            expense_id = st.text_input("Expense ID:")
            new_amount = st.number_input("New Amount:")
            new_description = st.text_input("New Description:")
            new_date = st.date_input("New Date:")

            if st.form_submit_button("Modify Expense"):
                success, message = modify_expenses(expense_id, new_amount, new_description, new_date)
                if success:
                    st.success(message)
                else:
                    st.error(message)    



if __name__ == "__main__":
    main()



