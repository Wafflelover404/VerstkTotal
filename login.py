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
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    return cursor.fetchone() is not None

# Function to verify login credentials
def verify_login(cursor, username, password):
    cursor.execute("SELECT 1 FROM users WHERE username = ? AND password = ?", (username, password))
    return cursor.fetchone() is not None

# Ensure the database directory exists
db_path = './Data/DB/app.db'
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

# Create or connect to the database and create tables
def initialize_database(db_path):
    with sqlite3.connect(db_path) as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                file_id INTEGER PRIMARY KEY AUTOINCREMENT,
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

initialize_database(db_path)

# Create new account tab
with tab1:
    st.subheader("Create a new account")
    create_username = st.text_input("Create a unique username", key="create_username")
    create_password = st.text_input("Create a password", type="password", key="create_password")
    
    if len(create_password) < 8:
        st.warning("Your password is shorter than 8 symbols.")
    
    if st.button("Create account"):
        if create_username and create_password:
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                if username_exists(cursor, create_username):
                    st.error("The username is occupied.")
                else:
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (create_username, create_password))
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

st.divider()

if st.session_state.account:
    st.header("My projects")
    st.write(f"Current account: {st.session_state.account}")
    with st.expander("Add files manually"):
        tab1, tab2 = st.tabs(["Upload file", "Write file manually"])
        with tab1:
            uploaded_file = st.file_uploader(label="Upload your html file here.")
            if uploaded_file is not None:
                # Read file content
                file_content = uploaded_file.getvalue()
                # Get filename
                filename = uploaded_file.name
                st.write(f"Uploaded file name: {filename}")
                st.write("File content:")
                st.write(file_content)
                if st.button("Add to database", key="upload_button"):
                    with sqlite3.connect(db_path) as db:
                        cursor = db.cursor()
                        cursor.execute("INSERT INTO files (filename, source) VALUES (?, ?)", (filename, file_content))
                        file_id = cursor.lastrowid
                        db.commit()
                        st.success(f"File added to the database with file_id: {file_id}")
        with tab2:
            st.write("Enter data.")
            file_name = st.text_input("filename", key="manual_filename")
            file_cont = st.text_area("content", key="manual_content")
            if st.button("Add to database", key="manual_button"):
                with sqlite3.connect(db_path) as db:
                    cursor = db.cursor()
                    cursor.execute("INSERT INTO files (filename, source) VALUES (?, ?)", (file_name, file_cont))
                    file_id = cursor.lastrowid
                    db.commit()
                    st.success(f"File added to the database with file_id: {file_id}")
        