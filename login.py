import streamlit as st
import sqlite3
import os

# Set page configuration
st.set_page_config(page_title="Authentication", layout="centered")

# Create a header for the app
st.header("Authentication")

# Create tabs for different login methods
tab1, tab2 = st.tabs(["Create new account", "Login to existing account"])

# Initialize session state
if 'account' not in st.session_state:
    st.session_state.account = ""

# Debugging function
def debug_print(message):
    st.text(message)

# Function to check if username exists
def username_exists(cursor, username):
    cursor.execute("SELECT 1 FROM users WHERE user = ?", (username,))
    return cursor.fetchone() is not None

# Function to verify login credentials
def verify_login(cursor, username, password):
    cursor.execute("SELECT 1 FROM users WHERE user = ? AND password = ?", (username, password))
    return cursor.fetchone() is not None

# Ensure the database directory exists
db_path = './Data/DB/users.db'
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

# Create or connect to the database
with sqlite3.connect(db_path) as db:
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, password TEXT)")
    db.commit()

# Create new account tab
with tab1:
    st.subheader("Create a new account")
    create_username = st.text_input("Create a unique username", key="create_username")
    create_password = st.text_input("Create a password", type="password", key="create_password")
    if len(create_password) < 8:
        st.warning("Your password is shorter than 8 symbols.")
    login = ""
    
    if st.button("Create account"):
        if create_username and create_password:
                with sqlite3.connect(db_path) as db:
                    cursor = db.cursor()
                    if username_exists(cursor, create_username):
                        st.error("The username is occupied.")
                    else:
                        cursor.execute("INSERT INTO users (user, password) VALUES (?, ?)", (create_username, create_password))
                        db.commit()
                        st.success("Account created successfully!")
                        st.session_state.account = create_username
                        debug_print(f"User: {create_username}, Password: {create_password} added to the database.")
        else:
            st.error("Please provide both a username and a password.")

# Login to existing account tab
with tab2:
    st.subheader("Login to existing account")
    login_username = st.text_input("Username", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login"):
        if login_username and login_password:
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                if verify_login(cursor, login_username, login_password):
                    st.success("Logged in successfully!")
                    st.session_state.account = login_username
                else:
                    st.error("Invalid username or password.")
        else:
            st.error("Please provide both username and password.")

# Hide Streamlit's default footer and menu
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Specify the path to your database file for projects
db_path = './Data/DB/projects.db'

# Create necessary tables in the projects database
with sqlite3.connect(db_path) as db:
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            file_id INTEGER PRIMARY KEY,
            filename TEXT NOT NULL,
            source TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_files (
            user_id INTEGER,
            file_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(file_id) REFERENCES files(file_id),
            PRIMARY KEY(user_id, file_id)
        )
    """)
    db.commit()