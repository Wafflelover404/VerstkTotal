import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import os
import json
import bcrypt

# Create a header for the app
st.header("Authentication")

# Create tabs for different login methods
tab1, tab2 = st.tabs(["Create new account", "Login to existing account"])

# Initialize session state
if 'account' not in st.session_state:
    st.session_state.account = ""

# Initialize session state
if 'account_id' not in st.session_state:
    st.session_state.account_id = ""

# Debugging function
def debug_print(message):
    st.text(message)

# Access via st.secrets dictionary
salt = st.secrets["salt"].encode('utf-8')  # Convert salt to bytes

def hash_it_quick(password):
    # converting password to array of bytes 
    bytes = password.encode('utf-8') 

    # Hashing the password 
    hash = bcrypt.hashpw(bytes, salt)

    # Return result 
    return hash

# Function to check if username exists
def username_exists(cursor, username):
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    return cursor.fetchone() is not None

# Function to verify login credentials
def verify_login(cursor, username, password):
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    if result:
        stored_hashed_password = result[0]
        return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password)
    return False

def get_user_id_by_username(cursor, username):
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_file_ids_by_user_id(cursor, user_id):
    cursor.execute("SELECT file_id FROM user_files WHERE user_id = ?", (user_id,))
    result = cursor.fetchall()
    return [row[0] for row in result] if result else []

def get_file_data_as_json(cursor, file_id):
    cursor.execute("SELECT filename, source FROM files WHERE file_id = ?", (file_id,))
    result = cursor.fetchone()
    
    if result:
        file_data = {
            "file_id": file_id,
            "filename": result[0],
            "content": result[1].decode('utf-8') if isinstance(result[1], bytes) else result[1]
        }
        return json.dumps(file_data, indent=4)
    else:
        return json.dumps({"error": "File not found"}, indent=4)

# Ensure the database directory exists
db_path = './Data/DB/app.db'
if not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path))

# Initialize session state
if 'db_path' not in st.session_state:
    st.session_state.db_path = db_path

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
    
    if len(create_password) < 8 and create_password != "":
        st.warning("Your password is shorter than 8 symbols.")
    
    if st.button("Create account"):
        if create_username and create_password:
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                if username_exists(cursor, create_username):
                    st.error("The username is occupied.")
                else:
                    hashed_password = hash_it_quick(create_password)
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (create_username, hashed_password))
                    st.success("Account created successfully!")
                    st.session_state.account = create_username
                    st.session_state.account_id = get_user_id_by_username(cursor, st.session_state.account)
                    debug_print(f"User: {create_username}, ID: {get_user_id_by_username(cursor, st.session_state.account)} added to the database.")
                    db.commit()
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
                    st.session_state.account_id = get_user_id_by_username(cursor, st.session_state.account)
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
        
        # Tab 1: Upload a file
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
                        cursor.execute("INSERT INTO user_files (user_id, file_id) VALUES (?, ?)", (get_user_id_by_username(cursor, st.session_state.account), file_id))
                        db.commit()
                        st.success(f"File added to the database with file_id: {file_id}")
        
        # Tab 2: Write file manually
        with tab2:
            st.write("Enter data manually.")
            filename = st.text_input("Filename", key="manual_filename")
            filecont = st.text_area("Content", key="manual_content")
            
            if st.button("Add to database", key="manual_button"):
                if filename and filecont:
                     with sqlite3.connect(db_path) as db:
                        cursor = db.cursor()
                        cursor.execute("INSERT INTO files (filename, source) VALUES (?, ?)", (filename, filecont))
                        file_id = cursor.lastrowid
                        cursor.execute("INSERT INTO user_files (user_id, file_id) VALUES (?, ?)", (get_user_id_by_username(cursor, st.session_state.account), file_id))
                        db.commit()
                        st.success(f"File added to the database with file_id: {file_id}")


    with st.expander("Existing projects"):
        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            user_id = get_user_id_by_username(cursor, st.session_state.account)
            file_ids = get_file_ids_by_user_id(cursor, user_id)
            
            if file_ids:
                # Create tabs for each file ID
                tabs = [f"File ID: {file_id}" for file_id in file_ids]
                selected_tab = st.tabs(tabs)
                
                for file_id, tab_name in zip(file_ids, tabs):
                    with selected_tab[tabs.index(tab_name)]:
                        file_json_str = get_file_data_as_json(cursor, file_id)
                        file_json = json.loads(file_json_str)  # Parse the JSON string into a dictionary
                        st.write(f"**File ID**: {file_id}")
                        st.write(f"**Filename**: {file_json['filename']}")
                        st.write("**File contents:**")
                        st.code(file_json["content"], line_numbers=True)
                        btn1, btn2 = st.columns(2)
                        with btn1:
                            # Create a button for downloading the file
                            if st.download_button(
                                    label="Export",
                                    data=file_json["content"],
                                    file_name=file_json['filename'],
                                    key=f"Download from bd{file_id}"
                                ):
                                st.success("Download started !")
                        with btn2:
                            if st.button(label="Edit", help="Open this file in code editor", key=f"{file_id}_export"):
                                st.session_state.edited_content = file_json["content"]
                                st.success("Opened in Web Editor !")
            else:
                st.write("No files found for this user.")
