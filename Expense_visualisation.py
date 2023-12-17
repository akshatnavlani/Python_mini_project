import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import sqlite3

#Reading the data
st.set_page_config(page_title="Bar Graph")
st.header("Bar Graph of expenses")

conn = sqlite3.connect('expenses.db')

query1 = "SELECT * FROM expenses"
df = pd.read_sql(query1, conn)

query2 = "SELECT category FROM expenses"
df_category = pd.read_sql(query2,conn)

conn.close()
st.dataframe(df)

#Pie-chart
pie_chart = px.pie(df_category,
                   title='Distribution of amount spent on various categories',
                   values='category',
                   names='category')

st.plotly_chart(pie_chart)

#Filters and selection
categories = df['category'].unique().tolist()
reasons = df['reason'].unique().tolist()

category_selection = st.multiselect('Category:',categories)
reason_selection = st.multiselect('Reason:', reasons)

date_selection = st.slider('Select start date', min_value=df['date'].min(), max_value=df['date'].max())

mask = (df['date'].between(*date_selection)) & (df['category'].isin(category_selection)) & (df['reason'].isin(reason_selection))
result_amount = df[mask].shape[0]
st.markdown(f'*Available results: {result_amount}*')

#Grouping the dataframe
df_income_grouped = df[mask].groupby(by=['income'])
df_expense_grouped = df[mask].groupby(by=['expense'])

#Bar charts
income_bar_chart = px.bar(df_income_grouped,
                          x='date',
                          y='income',
                          text='Income vs Time',
                          color_discrete_sequence=['#08653f'],
                          template='plotly_white')

expense_bar_chart = px.bar(df_expense_grouped,
                          x='date',
                          y='expense',
                          text='Expense vs Time',
                          color_discrete_sequence=['#08653f'],
                          template='plotly_white')


