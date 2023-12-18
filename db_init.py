import sqlite3

conn = sqlite3.connect("expense_db.db")
cursor = conn.cursor()

'''
Table columns:
transaction_id (random integer, also primary key, not null)
amount (float)
date (DATE)
reason (text field)
category (drop down) 
label (3 st buttons) Labels: rqd (required), cbp (could be prevented), nn (not needed)
'''

cursor.execute("CREATE TABLE IF NOT EXISTS expenses (transaction_id INTEGER PRIMARY KEY NOT NULL, amount REAL, date DATE, reason TEXT, category TEXT, label TEXT CHECK(label IN ('Required.', 'Could be prevented.', 'Not needed.')));")