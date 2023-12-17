import random
import string
import sqlite3

conn = sqlite3.connect("expense_db.db")
cursor = conn.cursor()

def is_transaction_id_unique(transaction_id, cursor):
    cursor.execute("SELECT COUNT(*) FROM expenses WHERE transaction_id = ?", (transaction_id,))
    count = cursor.fetchone()[0]
    return count == 0

def generate_unique_transaction_id(cursor):
    while True:
        transaction_id = ''.join(random.choice(string.digits) for i in range(6))
        if is_transaction_id_unique(transaction_id, cursor):
            return transaction_id



# unique_id = generate_unique_transaction_id(cursor)
# print(unique_id)