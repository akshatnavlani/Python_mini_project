import sqlite3

#Function to ADD expenses
def add_expenses(user_id, amount, description, date):
  conn=sqlite3.connect('user_data.db')
  cursor=conn.cursor()
  
  try:
    cursor.execute("INSERT INTO expenses (user_id, amount, description, date) VALUES (?,?,?,?)",(user_id, amount, description, date))
    conn.commit()
    conn.close()
    return True, "Expense added successfully."
  except sqlite3.Error as e:
    conn.close()
    return False, f"Error adding expense: {e}"
  
  
#Function to VIEW Expenses
# Function to view expenses
def view_expenses(user_id):
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    if user_id is not None:
        # Convert user_id to a tuple
        user_id_tuple = (user_id,)
        cursor.execute("SELECT * FROM expenses WHERE user_id=?", user_id_tuple)
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    else:
        conn.close()
        return []



#Function to MODIFY expenses
def modify_expenses(expense_id, amount,description,date):
  conn=sqlite3.connect("user_data.db")
  cursor=conn.cursor()
  
  try:
    cursor.execute("UPDATE expenses SET amount=?, description=?, date=? WHERE id=?",(amount, description, date, expense_id))    
    conn.commit()
    conn.close()
    return True, "Expense modified successfully."
  except sqlite3.Error as e:
    conn.close()
    return False, f"Error modifying expense: {e}"