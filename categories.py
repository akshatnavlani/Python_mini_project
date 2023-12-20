import sqlite3
import streamlit as st

def add_category(conn):
    cursor = conn.cursor()

    st.header("Add Category")

    new_category = st.text_input("New Category")
    default_color = "#000000"
    new_color = st.color_picker("Color", value=default_color)

    add_category_button = st.button("Add Category")

    success_message_shown = False

    if add_category_button and new_category and new_color:
        cursor.execute("INSERT OR REPLACE INTO categories (name, color) VALUES (?, ?)", (new_category, new_color))
        conn.commit()
        success_message_shown = True

    if success_message_shown:
        st.success(f"Category '{new_category}' added or updated successfully!")
        st.rerun()

def display_categories(conn):
    cursor = conn.cursor()

    st.header("Existing Categories")


    categories = cursor.execute("SELECT name, color FROM categories").fetchall()
    buttons_html = []
    for category, color in categories:
        button_html = (
            f'<button style="background-color: {color}; color: white; padding: 10px; margin: 5px; border: none; border-radius: 5px;">'
            f'{category}'
            '</button>'
        )
        buttons_html.append(button_html)

    st.markdown(" ".join(buttons_html), unsafe_allow_html=True)

def delete_category(conn):
    cursor = conn.cursor()

    st.header("Delete Category")

    delete_category = st.text_input("Delete Category")
    delete_category_button = st.button("Delete Category")

    if delete_category_button and delete_category:
        cursor.execute("DELETE FROM categories WHERE name=?", (delete_category,))
        conn.commit()
        st.success(f"Category '{delete_category}' deleted successfully!")
        st.rerun()

def main():
    conn = sqlite3.connect("expense_db.db")
    
    # db table fallback
    conn.execute('''CREATE TABLE IF NOT EXISTS categories
                    (name TEXT PRIMARY KEY, color TEXT)''')
    conn.commit()

    add_category(conn)
    display_categories(conn)
    delete_category(conn)

if __name__ == "__main__":
    main()