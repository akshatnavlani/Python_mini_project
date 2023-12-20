import sqlite3
import streamlit as st

def add_category(conn, username):
    cursor = conn.cursor()

    st.header("Add Category")

    new_category = st.text_input("New Category")
    default_color = "#000000"
    new_color = st.color_picker("Color", value=default_color)

    add_category_button = st.button("Add Category")

    success_message_shown = False

    if add_category_button and new_category and new_color:
        # Use a separate table for each user
        category_table_name = f"categories_{username}"
        
        # Create the table if it doesn't exist
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {category_table_name}
                           (name TEXT PRIMARY KEY, color TEXT)''')
        
        cursor.execute(f"INSERT OR REPLACE INTO {category_table_name} (name, color) VALUES (?, ?)", (new_category, new_color))
        conn.commit()
        success_message_shown = True

    if success_message_shown:
        st.success(f"Category '{new_category}' added or updated successfully!")

def display_categories(conn, username):
    cursor = conn.cursor()

    st.header("Existing Categories")

    # Use a separate table for each user
    category_table_name = f"categories_{username}"
    
    categories = cursor.execute(f"SELECT name, color FROM {category_table_name}").fetchall()
    buttons_html = []
    for category, color in categories:
        button_html = (
            f'<button style="background-color: {color}; color: white; padding: 10px; margin: 5px; border: none; border-radius: 5px;">'
            f'{category}'
            '</button>'
        )
        buttons_html.append(button_html)

    st.markdown(" ".join(buttons_html), unsafe_allow_html=True)

def delete_category(conn, username):
    cursor = conn.cursor()

    st.header("Delete Category")

    delete_category = st.text_input("Delete Category")
    delete_category_button = st.button("Delete Category")

    if delete_category_button and delete_category:
        # Use a separate table for each user
        category_table_name = f"categories_{username}"
        
        cursor.execute(f"DELETE FROM {category_table_name} WHERE name=?", (delete_category,))
        conn.commit()
        st.success(f"Category '{delete_category}' deleted successfully!")

def main():
    # Get the current username from session_state
    username = st.session_state.username

    # Check if the username is available
    if username is None:
        st.warning("Please log in to access this page.")
        return

    conn = sqlite3.connect("expense_db.db")

    # You might not need this table creation here
    # Use a separate table for each user
    category_table_name = f"categories_{username}"
    conn.execute(f'''CREATE TABLE IF NOT EXISTS {category_table_name}
                    (name TEXT PRIMARY KEY, color TEXT)''')
    conn.commit()

    add_category(conn, username)
    display_categories(conn, username)
    delete_category(conn, username)

if __name__ == "__main__":
    main()
