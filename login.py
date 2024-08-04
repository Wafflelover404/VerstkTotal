import streamlit as st
import sqlite3
import os

# Set page configuration
st.set_page_config(page_title="Authentication", layout="centered")

# Create a header for the app
st.header("Authentication")

# Create tabs for different login methods
tab1, tab2 = st.tabs(["Create new account", "Login to existing account"])

# Debugging function
def debug_print(message):
    st.text(message)

# Function to check if username exists
def username_exists(username):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute("SELECT 1 FROM users WHERE user = ?", (username,))
        return cursor.fetchone() is not None

# Ensure the database directory exists
db_path = './Data/DB/users.db'
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

# Create new account tab
with tab1:
    st.subheader("Create a new account")
    username = st.text_input("Create a unique username", key="create_username")
    password = st.text_input("Create a password", type="password", key="create_password")
    
    if st.button("Create account"):
        if username and password:
            try:
                with sqlite3.connect(db_path) as db:
                    cursor = db.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, password TEXT)")
                    
                    if username_exists(username):
                        st.error("The username is occupied.")
                    else:
                        cursor.execute("INSERT INTO users (user, password) VALUES (?, ?)", (username, password))
                        db.commit()
                        st.success("Account created successfully!")
                        debug_print(f"User: {username}, Password: {password} added to the database.")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please provide both a username and a password.")

# Login to existing account tab
with tab2:
    st.subheader("Login to existing account")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        # Here you would add logic to verify the username and password against the database
        st.success("Logged in successfully!")

# Hide Streamlit's default footer and menu
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)