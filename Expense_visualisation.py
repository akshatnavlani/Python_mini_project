import pandas as pd
import streamlit as st
import plotly.express as px
import datetime
from datetime import datetime
import sqlite3

#Reading the data
st.set_page_config(page_title="Statistics")
st.header("Statistics")
st.write("Dataframe")
conn = sqlite3.connect('expenses.db')

query1 = "SELECT * FROM expenses"
df = pd.read_sql(query1, conn)

query2 = "SELECT category FROM expenses"
df_category = pd.read_sql(query2,conn)

query3 = "SELECT label FROM expenses"
df_label = pd.read_sql(query3,conn)


conn.close()
st.dataframe(df)

#Pie-chart
category = df['category']
amount = df['amount']
pie_chart = px.pie(df_category,
                   title='Distribution of amount spent on various categories',
                   values=amount,
                   names=category,
                   color='category', 
                   color_discrete_map={row['category']: row['color'] for index, row in df.iterrows()})

st.plotly_chart(pie_chart)

#Date selection
dates = df['date'].unique().tolist()

df['date'] = pd.to_datetime(df['date'])

start_date = st.selectbox('Start date:',dates)
end_date = st.selectbox('End date:',dates)

filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

#Bar chart
st.header("Bar chart of expenses with time")

grouped_counts = df.groupby(['amount', 'label']).size().unstack(fill_value=0).stack()
columns_required = ['date','amount']
df2 = filtered_df[columns_required].copy()
df2_upd=df2.set_index("date")
st.bar_chart(df2_upd)
