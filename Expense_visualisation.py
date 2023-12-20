import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3

def page(username):
    st.header("Bar Graph of expenses")

    # Connect to the SQLite database
    conn = sqlite3.connect('expense_db.db')

    # Read data from expenses table for the specific user
    query1 = f"SELECT * FROM expenses WHERE username = '{username}'"
    df = pd.read_sql(query1, conn, parse_dates=['date'])  # Ensure 'date' column is parsed as datetime

    if df.empty:
        st.warning("No transactions available.")
        return

    # Read unique categories, colors, and sum of amounts for the specific user
    query_colors = f"SELECT DISTINCT category, color, SUM(amount) as amount FROM expenses WHERE username = '{username}' GROUP BY category, color"
    df_colors = pd.read_sql(query_colors, conn)

    # Close the database connection
    conn.close()

    # Pie-chart
    pie_chart = px.pie(df_colors,
                       title='Distribution of amount spent on various categories',
                       values='amount',
                       names='category',
                       color='category',  # Specify the 'category' column for coloring
                       color_discrete_map=dict(zip(df_colors['category'], df_colors['color'])))

    st.plotly_chart(pie_chart)

    # Filters and selection
    categories = df['category'].unique().tolist()
    reasons = df['reason'].unique().tolist()

    category_selection = st.multiselect('Category:', categories)

    # Date selection
    min_date, max_date = df['date'].min(), df['date'].max()

    if min_date == max_date:
        st.warning("Only one day of transactions available.")
        return

    # Convert datetime64 to regular Python datetime
    min_date, max_date = min_date.to_pydatetime(), max_date.to_pydatetime()

    # Unpack the tuple
    date_selection = st.slider('Select start date', min_value=min_date, max_value=max_date, value=(min_date, max_date))

    start_date, end_date = date_selection

    mask = (df['date'].between(start_date, end_date)) & (df['category'].isin(category_selection))
    result_amount = df[mask].shape[0]
    st.markdown(f'*Available results: {result_amount}*')

    # Bar charts
    amount_bar_chart = px.bar(df[mask],
                              x='date',
                              y='amount',
                              color='label',  # Use 'label' instead of 'category' for coloring
                              text='amount',
                              color_discrete_sequence=['#f2a90a', '#0af27e', '#e33939'],
                              template='plotly_white')

    st.plotly_chart(amount_bar_chart)

if __name__ == "__main__":
    # Check if a user is logged in before calling the page function
    if st.session_state.username:
        page(st.session_state.username)
